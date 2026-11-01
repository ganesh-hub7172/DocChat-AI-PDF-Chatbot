# 📚 DocChat AI – PDF Semantic Search

DocChat AI is a Python and Streamlit application that lets users upload a text-based PDF and retrieve relevant passages by asking questions in natural language.

## Features

- Upload PDF documents through a Streamlit interface
- Extract selectable text with PyPDF
- Split document text into overlapping chunks
- Generate local text embeddings with Sentence Transformers
- Store vectors in ChromaDB
- Retrieve relevant passages using semantic similarity

> **Current scope:** This repository implements PDF processing and semantic retrieval (the retrieval part of RAG). It does not yet generate LLM-written answers. The app displays the most relevant passages so users can inspect the source text.

## Tech stack

- Python
- Streamlit
- PyPDF
- Sentence Transformers (`all-MiniLM-L6-v2`)
- ChromaDB

## Project structure

```text
DocChat-AI-PDF-Chatbot/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── data/
│   └── .gitkeep
└── utils/
    ├── __init__.py
    ├── pdf_processor.py
    └── rag_pipeline.py
```

The `.venv/` and `chroma_db/` folders are created locally and intentionally excluded from Git.

## Run locally (Windows PowerShell)

1. Install Python 3.10 or newer.
2. Clone this repository and enter the folder:

   ```powershell
   git clone YOUR_REPOSITORY_URL
   cd DocChat-AI-PDF-Chatbot
   ```

3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

6. Open the local URL shown in the terminal (usually `http://localhost:8501`).

The first run downloads the Sentence Transformers embedding model, so it may take a few minutes and requires an internet connection.

## How it works

```text
PDF upload
   ↓
Text extraction (PyPDF)
   ↓
Text chunking with overlap
   ↓
Embedding generation (Sentence Transformers)
   ↓
Vector storage (ChromaDB)
   ↓
Semantic search
   ↓
Relevant passages displayed in Streamlit
```

## Limitations

- Scanned/image-only PDFs need OCR; OCR is not included.
- The current app indexes one uploaded PDF at a time.
- The current version retrieves passages but does not generate natural-language answers with an LLM.
- The embedding model is downloaded on first use.

## Roadmap

- LLM-generated answers grounded in retrieved passages
- Conversational chat history
- Page-level citations for retrieved passages
- Multi-PDF collections
- Automated tests and deployment

## Author

**Ganesh Musham**

GitHub: [ganesh-hub7172](https://github.com/ganesh-hub7172)
