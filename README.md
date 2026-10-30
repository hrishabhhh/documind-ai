# DocuMind AI

**An AI-powered document question-answering system built using Python, FastAPI, Sentence Transformers, and Google Gemini.**

DocuMind AI is a Retrieval-Augmented Generation (RAG) application that allows users to ask natural-language questions about PDF documents and receive context-aware answers grounded in retrieved document content.

The project is being developed incrementally, with a focus on understanding RAG architecture, semantic search, document processing, metadata management, and production-oriented backend design.

## Project Status

**Current stage: Functional RAG backend with section-aware document processing.**

The application can currently:

- Extract text from PDF documents.
- Split extracted text into overlapping chunks.
- Generate semantic embeddings.
- Perform vector similarity search.
- Retrieve relevant document chunks.
- Filter search results by similarity score.
- Expand retrieved context using neighboring chunks.
- Detect structured document sections from PDF headings.
- Attach section metadata to document chunks.
- Generate document-grounded answers using Google Gemini.
- Include source page references in generated answers.

**Currently implemented:** In-memory RAG processing and section metadata generation.

**In progress:** Section-based retrieval across multiple PDF pages.

**Planned:** Persistent vector storage, document upload APIs, automated tests, and a Next.js frontend.

---

## Tech Stack

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python 3.11           | Backend development             |
| FastAPI               | Backend API framework           |
| PyMuPDF               | PDF text extraction             |
| Sentence Transformers | Text embedding generation       |
| all-MiniLM-L6-v2      | Local embedding model           |
| NumPy                 | Vector similarity calculations  |
| Google Gemini         | LLM-based answer generation     |
| Google GenAI SDK      | Gemini API integration          |
| python-dotenv         | Environment variable management |
| Git / GitHub          | Version control                 |

## Architecture

DocuMind AI follows a modular service-based architecture.

### Document Ingestion Pipeline

```text
PDF Document
      |
      v
DocumentService
      |
      |-- Extract text from pages
      |-- Detect document sections
      |-- Split text into overlapping chunks
      |-- Attach chunk metadata
      |
      v
IngestionService
      |
      |-- Generate vector embeddings
      |
      v
In-Memory Chunk Collection
      |
      |-- Text
      |-- Embedding
      |-- Page number
      |-- Chunk ID
      |-- Chunk index
      |-- Section metadata
```

### Question-Answering Pipeline

```text
User Question
      |
      v
RAGService
      |
      v
SearchService
      |
      |-- Generate query embedding
      |-- Compute similarity scores
      |-- Retrieve top-K chunks
      |
      v
Similarity Filtering
      |
      v
Same-Page Context Expansion
      |
      v
Context Construction
      |
      v
GeminiService
      |
      |-- Combine question and context
      |-- Generate grounded answer
      |
      v
AI-Generated Answer
```

**Note:** Section metadata is generated during document processing, but full section-based retrieval has not yet been integrated into the RAG question-answering pipeline.

---

## Implemented Features

### 1. PDF Text Extraction

Implemented using PyMuPDF.

The `DocumentService` reads PDF documents and extracts text from individual pages.

Each extracted page contains:

```python
{
    "page_number": 6,
    "text": "Extracted document content..."
}
```

**Features:**

- Page-by-page text extraction.
- Page number preservation.
- Empty text page filtering.
- Structured output for subsequent processing.

### 2. Document Chunking

Extracted text is divided into smaller, overlapping chunks to improve semantic retrieval.

**Current default configuration:**

```python
chunk_size = 500
overlap = 100
```

Overlapping chunks help preserve context near chunk boundaries.

The chunking algorithm uses string slicing and a configurable step size.

### 3. Section Detection and Metadata

Implemented heading-based document section detection.

The current detector identifies weekday workout sections by examining the first line of each PDF page.

For example:

```text
TUESDAY / 1 OF 2
TUESDAY / 2 OF 2
```

Both pages are recognized as belonging to the `tuesday` section.

**Verified section mapping:**

```python
{
    4: "monday",
    5: "monday",
    6: "tuesday",
    7: "tuesday",
    8: "wednesday",
    9: "wednesday",
    10: "thursday",
    11: "thursday",
    12: "friday",
    13: "friday",
    14: "saturday",
    15: "saturday"
}
```

The detector processes already-extracted pages, avoiding repeated PDF extraction for every weekday.

Each processed chunk now includes structured metadata:

```python
{
    "chunk_id": 23,
    "page_number": 6,
    "chunk_index": 0,
    "section": "tuesday",
    "text": "Barbell back squat..."
}
```

This enables future metadata-aware and section-based retrieval.

**Current limitation:** The detector recognizes headings following the sample workout PDF's weekday format. It is not yet a general-purpose section parser for arbitrary documents.

### 4. Embedding Generation

Implemented using Sentence Transformers and the `all-MiniLM-L6-v2` model.

Each chunk is converted into a **384-dimensional vector embedding**.

Embeddings are normalized during generation to support efficient cosine-similarity ranking through vector dot products.

### 5. Semantic Search

Implemented in `SearchService`.

The system:

1. Generates an embedding for the user's query.
2. Compares it against indexed document embeddings.
3. Calculates similarity scores using NumPy.
4. Sorts chunks by similarity.
5. Returns the top-K matching chunks with their metadata.

**Example retrieval:**

```text
Query: What should I do on Tuesday?

Chunk 23 | Page 6  | Score 0.2111
Chunk 69 | Page 17 | Score 0.1645
Chunk 70 | Page 17 | Score 0.1617
```

Search results include chunk IDs, source page numbers, similarity scores, and retrieved text.

### 6. Similarity Filtering

Implemented an experimental relevance threshold in `RAGService`.

```python
filtered_results = [
    result
    for result in results
    if result["score"] >= 0.20
]
```

This reduces the number of weak semantic matches included in the LLM context.

If no results pass the threshold, the system returns a fallback response.

**Current limitation:** The threshold of `0.20` is experimental and may reject useful information for other questions or documents. It requires further evaluation before production use.

### 7. Context Expansion

Implemented `expand_results()` in `SearchService`.

The method retrieves neighboring document chunks around relevant semantic matches.

**Features:**

- Configurable expansion window.
- Duplicate prevention using Python sets.
- Same-page boundary checks.
- Ordering by original chunk ID.
- Preservation of original matching chunks.

Example:

```text
Original match:
Chunk 23

Expanded result:
Chunk 23
Chunk 24
```

Context expansion provides additional text surrounding a matched chunk, helping the language model generate more complete answers.

### 8. Google Gemini Integration

Implemented `GeminiService` using the Google GenAI Python SDK.

**Responsibilities:**

- Load API credentials from environment variables.
- Initialize the Gemini client.
- Send prompts to the configured language model.
- Return generated text.

The project has been tested with `gemini-3.8-flash`.

Temporary Gemini service availability errors were encountered during development. Retry handling can be used for transient failures.

### 9. Retrieval-Augmented Question Answering

Implemented `RAGService` to orchestrate semantic search, filtering, context expansion, prompt creation, and LLM generation.

The prompt instructs Gemini to:

- Answer using the supplied document context.
- Avoid inventing unsupported information.
- Mention source page numbers.
- Return a fallback response when the context is insufficient.
- Treat retrieved document content as reference material rather than instructions.

**Example question:**

```text
What should I do on Tuesday?
```

**Example generated answer:**

```text
Based on Page 6, Tuesday's workout consists of
Squat + quads / hamstrings training.

Exercises:

1. Barbell back squat
   3 sets × 6–8 reps
   Rest: 180 seconds

2. Seated leg curl
   4 sets × 10–15 reps
   Rest: 90–120 seconds
```

This result was generated successfully during manual testing.

The RAG pipeline currently runs locally using in-memory embeddings and document chunks.

**Source citations are prompt-generated rather than independently validated.** More robust citation validation is planned.

---

## Project Structure

```text
documind-ai/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   └── services/
│   │       ├── document_service.py
│   │       ├── embedding_service.py
│   │       ├── ingestion_service.py
│   │       ├── search_service.py
│   │       ├── gemini_service.py
│   │       └── rag_service.py
│   │
│   ├── tests/
│   │   ├── test_section_manual.py
│   │   ├── test_chunk_metadata_manual.py
│   │   ├── test_pdf_search_manual.py
│   │   ├── test_search_manual.py
│   │   ├── test_gemini_manual.py
│   │   └── test_rag_manual.py
│   │
│   ├── data/
│   │   └── sample.pdf
│   │
│   ├── requirements.txt
│   ├── .env
│   └── venv/
│
├── .gitignore
└── README.md
```

_Structure reflects the backend development files used so far. Local environment files and sample documents may not be tracked in Git._

---

## Local Setup

### Prerequisites

- Python 3.11
- Git
- Google Gemini API key

### 1. Clone the repository

```bash
git clone <repository-url>
cd documind-ai/backend
```

Replace `<repository-url>` with the actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows — Git Bash**

```bash
source venv/Scripts/activate
```

**Windows — PowerShell**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

Major dependencies include:

```text
fastapi
uvicorn
pymupdf
sentence-transformers
numpy
google-genai
python-dotenv
```

### 5. Configure environment variables

Create a `.env` file inside `backend/`:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit your `.env` file or expose your API credentials.

### 6. Run the FastAPI backend

From `backend/`:

```bash
uvicorn app.main:app --reload
```

Available basic endpoints:

```text
GET /
GET /health
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Document upload and RAG question-answering endpoints are not implemented yet.

---

## Manual Testing

Run these commands from the `backend/` directory with the virtual environment activated.

### Section Detection

```bash
python -m tests.test_section_manual
```

Validates page-to-section mapping for the sample PDF.

### Chunk Metadata

```bash
python -m tests.test_chunk_metadata_manual
```

Validates chunk IDs, page numbers, and section metadata.

### Semantic Search

```bash
python -m tests.test_pdf_search_manual
```

Tests PDF ingestion, embedding generation, semantic similarity, and retrieval.

### Gemini Integration

```bash
python -m tests.test_gemini_manual
```

Tests language model connectivity and answer generation.

### End-to-End RAG

```bash
python -m tests.test_rag_manual
```

Runs document ingestion, retrieval, context construction, and Gemini answer generation.

**Note:** These are development-time manual tests. A comprehensive automated test suite has not yet been completed.

---

## Known Limitations

1. **In-memory storage:** Embeddings and chunks are not yet persisted in a vector database.
2. **Incomplete multi-page answers:** The RAG pipeline currently expands neighboring chunks within individual pages, not complete logical sections.
3. **Document-specific section detection:** Current heading recognition is tailored to the workout PDF.
4. **Experimental similarity threshold:** The fixed threshold requires evaluation on diverse queries.
5. **No document upload API:** PDF paths are currently provided directly in local test workflows.
6. **No conversation history:** Each RAG question is processed independently.
7. **No frontend:** User-facing document upload and chat interfaces have not been implemented.
8. **Unverified generated citations:** Page references are requested through prompting, but are not programmatically checked.

---

## Development Roadmap

### Completed

- [x] FastAPI backend foundation
- [x] PDF text extraction
- [x] Overlapping text chunking
- [x] Local embedding generation
- [x] Semantic similarity search
- [x] Gemini LLM integration
- [x] End-to-end RAG question answering
- [x] Global chunk identifiers
- [x] Similarity-based retrieval filtering
- [x] Neighboring context expansion
- [x] Document heading inspection
- [x] Weekday section detection
- [x] Page-to-section mapping
- [x] Section metadata attached to chunks
- [x] Manual section and retrieval tests

### Upcoming

- [ ] Implement `get_chunks_by_section()` in `SearchService`
- [ ] Integrate section-aware retrieval into `RAGService`
- [ ] Retrieve complete document sections across pages
- [ ] Add configurable context-size limits
- [ ] Improve relevance filtering and retrieval evaluation
- [ ] Implement verified document citations
- [ ] Integrate Supabase PostgreSQL and pgvector
- [ ] Store documents, chunks, embeddings, and metadata persistently
- [ ] Build FastAPI document upload endpoints
- [ ] Build FastAPI question-answering endpoints
- [ ] Add document-level isolation and validation
- [ ] Create automated unit and integration tests
- [ ] Build Next.js frontend
- [ ] Implement document upload and chat UI
- [ ] Add authentication and user-specific document management
- [ ] Deploy the application

---

## Future Architecture

```text
Next.js Frontend
      |
      v
FastAPI Backend
      |
      |-- Document Upload API
      |-- Document Processing
      |-- Embedding Generation
      |-- Section-Aware Retrieval
      |-- RAG Orchestration
      |
      v
Supabase PostgreSQL + pgvector
      |
      |-- Documents
      |-- Chunks
      |-- Embeddings
      |-- Metadata
      |
      v
Google Gemini
      |
      v
Grounded Answer + Source References
```

---

## Learning Objectives

DocuMind AI is also a hands-on project for learning:

- Python programming and object-oriented design.
- Modular backend architecture.
- Data structures such as lists, dictionaries, and sets.
- Text processing, document parsing, and metadata extraction.
- Vector embeddings and semantic similarity.
- Retrieval-Augmented Generation architecture.
- Prompt engineering and LLM integration.
- Algorithm design, debugging, testing, and refactoring.
- Persistent vector storage and production API development.

The project emphasizes understanding **why an algorithm or architectural decision is used**, rather than only implementing code.

---

## Security Notes

- Store API keys in environment variables.
- Keep `.env` and virtual environment files out of version control.
- Do not log secrets or raw credentials.
- Validate uploaded file types and sizes when upload APIs are implemented.
- Treat document content as untrusted input.
- Add authentication, document authorization, and resource limits before production deployment.

---

## Current Milestone

**Milestone 8C — Section-Aware Document Processing: Completed**

The backend now extracts document structure and attaches logical section metadata to chunks.

**Next milestone: Section-Based Retrieval**

Implement a retrieval method that can return all chunks belonging to a selected section, allowing the RAG pipeline to answer questions using content spanning multiple PDF pages.

---

## Author

Developed as a hands-on AI engineering and Retrieval-Augmented Generation project.

**Project:** DocuMind AI

**Development status:** Active
