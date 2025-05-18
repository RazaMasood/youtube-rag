from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableMap
from pydantic import BaseModel


class CustomStrOutputParser(StrOutputParser):
    model_config = {
        "arbitrary_types_allowed": True
    }

    def parse(self, text):
        # Always return a string, even if input is a list
        if isinstance(text, list):
            return "\n".join(str(t) for t in text)
        return str(text)

    def __call__(self, text):
        return self.parse(text)

    @property
    def lc_serializable(self):
        return False


def setup_qa_chain(
    transcript: str,
    temperature: float = 0.5,
    model: str = "mistral",
    chunk_size: int = 1500,
    chunk_overlap: int = 200
):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_text(transcript)
        if not chunks:
            return None, "No content to process after splitting."

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

        llm = OllamaLLM(model=model, temperature=temperature)
        parser = CustomStrOutputParser()

        def format_docs(docs):
            if not docs:
                return "NO_CONTEXT"
            return "\n\n---\n\n".join(doc.page_content for doc in docs)

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are a helpful assistant.
Answer ONLY from the provided transcript context.
If the context is insufficient, just say: "This topic is not discussed in the video."

### CONTEXT FROM VIDEO TRANSCRIPT:
{context}

### IMPORTANT INSTRUCTIONS:
- If CONTEXT is "NO_CONTEXT", respond exactly with: "This topic is not discussed in the video."
- Do NOT guess or use outside knowledge.
- Be concise.

### Question: {question}

### Answer:
"""
        )

        chain = (
            RunnableMap({
                "context": RunnableLambda(lambda x: retriever.invoke(x["question"])) | RunnableLambda(format_docs),
                "question": RunnableLambda(lambda x: x["question"])
            })
            | prompt
            | llm
            | parser
        )

        return chain, None

    except Exception as e:
        return None, f"Error setting up QA chain: {str(e)}"


def answer_question(qa_chain, question: str) -> str:
    try:
        result = qa_chain.invoke({"question": question})
        # Ensure output is a string (sometimes can be a list)
        if isinstance(result, list):
            return "\n".join(result)
        return str(result)
    except Exception as e:
        return f"Error generating answer: {str(e)}"
