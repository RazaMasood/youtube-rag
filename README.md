# 🎥 AskMyVideo - AI Video Analysis & Chat Tool

**Transform YouTube videos into interactive AI conversations | Ask questions, get insights, extract key information**

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral%207B-green)](https://ollama.ai)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

![AskMyVideo Demo 1](assets/1.png)
![AskMyVideo Demo 2](assets/2.png)
![AskMyVideo Demo 2](assets/3.png)

## ✨ Features

- **YouTube Video Analysis**: Automatically extracts and processes transcripts from any YouTube video
- **AI-Powered Q&A**: Ask questions about video content and get accurate, context-aware answers
- **Multi-Language Support**: Works with videos in 10+ languages including English, Spanish, French, German, and more
- **Interactive UI**: Clean, intuitive interface with real-time responses
- **Export Functionality**: Save your conversations for later reference
- **Suggested Questions**: Get started quickly with pre-defined question suggestions

## 🚀 Getting Started

### Prerequisites

- Python 3.11
- Streamlit (For UI)
- Ollama (with Mistral 7B model installed and nomic-embed-text for embeddings)
- youtube-transcript-api library for transcript extraction
- LangChain framework for RAG (Retrieval-Augmented Generation)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/RazaMasood/AskMyVideo.git
   cd askmyvideo
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application
   ```bash
   streamlit run app.py
   ```

## 📋 How to Use

1. **Load a Video**: Paste a YouTube URL in the sidebar input field
2. **Select Language**: Choose the language of the video transcript
3. **Process Video**: Click "Process Video" to extract and analyze the content
4. **Ask Questions**: Type your questions about the video in the main chat area
5. **Review Answers**: Get AI-generated responses based on the video content
6. **Export Conversation**: Download your Q&A session for future reference

## 🔍 How It Works

1. **Transcript Extraction**: The app extracts the transcript from the provided YouTube video
2. **Text Processing**: The transcript is processed and embedded using Nomic for semantic search
3. **RAG Pipeline**: Uses a Retrieval-Augmented Generation approach to find relevant sections of the transcript
4. **Ollama Integration**: Sends context and queries to locally-hosted Mistral 7B model via Ollama
5. **Response Generation**: Delivers accurate answers based on the retrieved context

## 📁 Project Structure

```
askmyvideo/
├── app.py                  # Main Streamlit application file
├── assets/
├── modules/
│   ├── transcript.py       # Transcript extraction functionality
│   ├── rag_pipeline.py     # RAG (Retrieval Augmented Generation) setup
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## 🛠️ Technologies Used

- **Streamlit**: For the web interface
- **LangChain**: For the RAG pipeline
- **Ollama**: For running Mistral 7B locally
- **Mistral 7B**: Open-source LLM for natural language processing
- **Nomic Embeddings**: For semantic text embeddings
- **YouTube API**: For transcript extraction
- **Vector Database**: For efficient semantic search

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
