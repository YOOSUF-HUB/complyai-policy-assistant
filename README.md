# ComplyAI - AI Policy & Document Compliance Assistant

ComplyAI is a Retrieval-Augmented Generation (RAG) based web application that helps users analyze policy, rules, legal, and compliance documents.

Users can upload a PDF document and use AI-powered workflows to:

- Ask questions from the document
- Summarize key rules
- Generate compliance checklists
- Identify risks and violations
- Generate concise compliance reports

---

## Project Objective

Long policy and compliance documents are difficult to read, understand, and act on. Users often miss important rules, deadlines, restrictions, and risks.

ComplyAI solves this by converting complex documents into clear, structured, and actionable outputs using RAG and AI workflows.

---

## Key Features

### 1. PDF Upload and Text Extraction

Users can upload a PDF document. The system extracts readable text using PyPDF.

### 2. Text Chunking

The extracted text is split into smaller overlapping chunks. This improves retrieval accuracy and avoids sending the full document to the AI model.

### 3. Embeddings and Vector Store

Each text chunk is converted into an embedding using Gemini embeddings. The embeddings are stored in FAISS for similarity search.

### 4. RAG-Based Question Answering

Users can ask questions about the uploaded document. The system retrieves the most relevant chunks and generates an answer using Gemini.

### 5. Compliance Workflows

The system provides structured AI workflows:

- Summarize Rules
- Generate Compliance Checklist
- Find Risks
- Generate Compliance Report

### 6. Source Evidence

For question answering, the app displays the source chunks used to generate the answer.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | HTML, Bootstrap |
| AI Model | Gemini |
| Embeddings | Gemini Embeddings |
| Vector Store | FAISS |
| PDF Processing | PyPDF |
| Environment | Python venv |
| Language | Python |

---

## System Architecture

```text
User
 ↓
Upload PDF
 ↓
FastAPI Backend
 ↓
PDF Text Extraction
 ↓
Text Chunking
 ↓
Gemini Embeddings
 ↓
FAISS Vector Store
 ↓
Question / Compliance Task
 ↓
Relevant Chunk Retrieval
 ↓
Gemini Answer Generation
 ↓
AI Output + Source Evidence
```

---

## RAG Pipeline

```text
1. Extract text from PDF
2. Split text into overlapping chunks
3. Generate embeddings for each chunk
4. Store embeddings in FAISS
5. Convert user question into an embedding
6. Retrieve similar chunks
7. Send retrieved chunks to Gemini
8. Generate grounded response
```

---

## Folder Structure

```text
complyai-policy-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── pdf_reader.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   └── ai_service.py
│
├── templates/
│   └── index.html
│
├── uploads/
├── docs/
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/complyai-policy-assistant.git
cd complyai-policy-assistant
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 2. Create a virtual environment

For macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Do not commit `.env` to GitHub.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Open in your browser:

```text
http://127.0.0.1:8000
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | Gemini API key used for embeddings and answer generation |

---

## How It Works

### Step 1: Upload PDF

The user uploads a policy, rules, legal, or compliance PDF.

### Step 2: Extract Text

The system extracts readable text from the PDF using PyPDF.

### Step 3: Split Text into Chunks

The extracted text is split into smaller overlapping chunks to improve retrieval.

### Step 4: Generate Embeddings

Each chunk is converted into a numerical vector using Gemini embeddings.

### Step 5: Store in FAISS

The vectors are stored in a FAISS index for similarity search.

### Step 6: Ask a Question or Run Workflow

The user can ask a document-specific question or run a compliance workflow.

### Step 7: Retrieve Relevant Context

The system retrieves the most relevant chunks from FAISS.

### Step 8: Generate AI Output

Gemini generates an answer, checklist, risk analysis, summary, or report based on the document context.

---

## Compliance Workflows

ComplyAI includes four structured workflows:

### Summarize Rules

Summarizes the key rules, requirements, restrictions, deadlines, and important conditions from the uploaded document.

### Generate Compliance Checklist

Converts the document into an actionable checklist.

### Find Risks

Identifies possible compliance risks, rule violations, penalties, disqualification conditions, and mistakes users may make.

### Generate Compliance Report

Creates a concise professional compliance analysis report.

---

## Example Use Cases

ComplyAI can be used for:

- Competition rulebooks
- University policies
- Internship guidelines
- Company policy documents
- HR manuals
- Legal agreements
- Healthcare SOPs
- Financial compliance documents
- Government circulars

---

## Current Limitations

- Uploaded documents are stored temporarily.
- Vector store is stored in memory.
- No user authentication.
- No persistent database yet.
- Works best with text-based PDFs, not scanned image PDFs.
- Large PDFs may take longer because embeddings are generated for each chunk.
- Compliance workflows currently use the extracted document text directly and do not yet cite exact page numbers.

---

## Future Improvements

- Add SQLite database for document history
- Add export-to-PDF for compliance reports
- Add OCR support for scanned PDFs
- Add multi-document support
- Add user authentication
- Add chat history
- Add better source citations
- Add downloadable compliance checklist
- Add page-level source tracking
- Add document comparison workflow
- Add risk scoring system

---

## Competition Relevance

ComplyAI demonstrates:

- RAG architecture
- AI-powered document analysis
- Agentic-style compliance workflows
- Source-grounded answer generation
- Structured output generation
- Practical real-world problem solving
- FastAPI backend development
- Gemini API integration
- FAISS vector search

This makes it suitable for AI hackathons where participants are expected to build intelligent document-processing or workflow-based AI systems.

---

## Git Workflow

Common commands used during development:

```bash
git status
git add .
git commit -m "your commit message"
git push
```

Before starting work:

```bash
git pull origin main
```

---

## License

This project is for learning only.