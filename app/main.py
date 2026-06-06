from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.pdf_reader import extract_text_from_pdf
from app.text_splitter import split_text_into_chunks


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


def render_home(
    request: Request,
    filename=None,
    text_preview=None,
    message=None,
    error=None,
    chunk_count=0,
    sample_chunks=None
):
    """
    Reusable function to render the homepage.
    """
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
            "sample_chunks": sample_chunks or []
        }
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render_home(
        request=request,
        filename=CURRENT_DOCUMENT["filename"],
        chunk_count=len(CURRENT_DOCUMENT["chunks"]),
        sample_chunks=CURRENT_DOCUMENT["chunks"][:3]
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    """
    Handle PDF upload, save it, extract text, split text into chunks,
    and display preview.
    """

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

        CURRENT_DOCUMENT["filename"] = file.filename
        CURRENT_DOCUMENT["text"] = extracted_text
        CURRENT_DOCUMENT["chunks"] = chunks

        return render_home(
            request=request,
            filename=file.filename,
            text_preview=extracted_text[:2000],
            message="PDF uploaded, text extracted, and chunks created successfully.",
            chunk_count=len(chunks),
            sample_chunks=chunks[:3]
        )

    except Exception as error:
        return render_home(
            request=request,
            error=str(error)
        )