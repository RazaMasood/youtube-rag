from fastapi import APIRouter
from modules.rag_pipeline import setup_qa_chain, answer_question
from model.rag_pipeline import RagRequest, RagResponse

# Default RAG configuration (move to env/config in production)
DEFAULT_TEMPERATURE = 0.5
DEFAULT_MODEL = "mistral"
DEFAULT_CHUNK_SIZE = 1500
DEFAULT_CHUNK_OVERLAP = 200

router = APIRouter(tags=["rag-pipeline"])

@router.post("/rag-qa", response_model=RagResponse)
def rag_qa(request: RagRequest):
    transcript = request.transcript
    question = request.question
    qa_chain, error = setup_qa_chain(
        transcript=transcript,
        temperature=DEFAULT_TEMPERATURE,
        model=DEFAULT_MODEL,
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP
    )
    if error or qa_chain is None:
        return RagResponse(answer=None, error=error)
    answer = answer_question(qa_chain, question)
    return RagResponse(answer=answer, error=None)
