from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.pdf_reader import extract_text_from_pdf
from app.text_splitter import split_text_into_chunks
from app.vector_store import build_faiss_index


app = FastAPI(title="ComplyAI - AI Policy Compliance Assistant")

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

UPLOAD_DIR.mkdir(exist_ok=True)


CURRENT_DOCUMENT = {
    "filename": None,
    "text": None,
    "chunks": []
}

VECTOR_STORE = {
    "index": None,
    "chunks": [],
    "embedding_count": 0,
    "dimension": 0
}


def render_home(
    request: Request,
    filename=None,
    text_preview=None,
    message=None,
    error=None,
    chunk_count=0,
    sample_chunks=None,
    embedding_count=0,
    vector_dimension=0
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": "ComplyAI",
            "subtitle": "AI Policy & Document Compliance Assistant",
            "filename": filename,
            "text_preview": text_preview,
            "message": message,
            "error": error,
            "chunk_count": chunk_count,
            "sample_chunks": sample_chunks or [],
            "embedding_count": embedding_count,
            "vector_dimension": vector_dimension
        }
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render_home(
        request=request,
        filename=CURRENT_DOCUMENT["filename"],
        chunk_count=len(CURRENT_DOCUMENT["chunks"]),
        sample_chunks=CURRENT_DOCUMENT["chunks"][:3],
        embedding_count=VECTOR_STORE["embedding_count"],
        vector_dimension=VECTOR_STORE["dimension"]
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            return render_home(
                request=request,
                error="Please upload a valid PDF file."
            )

        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / unique_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = extract_text_from_pdf(str(file_path))

        if not extracted_text:
            return render_home(
                request=request,
                filename=file.filename,
                error="PDF uploaded, but no readable text was found."
            )

        chunks = split_text_into_chunks(
            text=extracted_text,
            chunk_size=900,
            overlap=150
        )

        vector_store = build_faiss_index(chunks)

        CURRENT_DOCUMENT["filename"] = file.filename
        CURRENT_DOCUMENT["text"] = extracted_text
        CURRENT_DOCUMENT["chunks"] = chunks

        VECTOR_STORE["index"] = vector_store["index"]
        VECTOR_STORE["chunks"] = vector_store["chunks"]
        VECTOR_STORE["embedding_count"] = vector_store["embedding_count"]
        VECTOR_STORE["dimension"] = vector_store["dimension"]

        return render_home(
            request=request,
            filename=file.filename,
            text_preview=extracted_text[:2000],
            message="PDF uploaded, text extracted, chunks created, and vector store built successfully.",
            chunk_count=len(chunks),
            sample_chunks=chunks[:3],
            embedding_count=VECTOR_STORE["embedding_count"],
            vector_dimension=VECTOR_STORE["dimension"]
        )

    except Exception as error:
        return render_home(
            request=request,
            error=str(error)
        )