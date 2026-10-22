# DocuMind AI 🧠

An AI-powered document intelligence application built using **Retrieval-Augmented Generation (RAG)** to enable semantic search and context-aware question answering over PDF documents.

## Tech Stack

- **Backend:** Python, FastAPI
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **PDF Processing:** PyMuPDF
- **Vector Operations:** NumPy
- **Planned:** Next.js, Gemini LLM, Supabase PostgreSQL with pgvector

## Features Implemented

- **PDF Text Extraction:** Extract text from PDFs while preserving page numbers.
- **Document Chunking:** Split extracted text into smaller, overlapping chunks.
- **Embedding Generation:** Convert text chunks into 384-dimensional normalized vectors.
- **Semantic Search:** Retrieve relevant text using cosine similarity.
- **Document Ingestion Pipeline:** Integrate PDF extraction, chunking, and embedding generation.
- **Manual Testing:** Test individual services and the document ingestion pipeline.

## Project Structure

```text
backend/
├── app/
│   ├── main.py
│   └── services/
│       ├── document_service.py
│       ├── embedding_service.py
│       ├── ingestion_service.py
│       └── search_service.py
├── tests/
├── data/
└── requirements.txt
```

## Run Locally

```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

_On Windows PowerShell, activate the environment using `venv\Scripts\Activate.ps1`._

## Current Progress

**PDF → Text Extraction → Chunking → Embeddings**

The document ingestion pipeline is implemented. Semantic search currently uses sample documents; connecting it to ingested PDF chunks is the next milestone.

## Upcoming Features

- Semantic search over uploaded PDF content
- Vector storage using PostgreSQL + pgvector
- Gemini-powered question answering with source citations
- PDF upload APIs and authentication
- Next.js frontend and deployment

---

**Project Status:** In active development.
