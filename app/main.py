from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.pdf_reader import extract_text_from_pdf


app = FastAPI(title="ComplyAI - AI Policy Compliance Assistant")

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

UPLOAD_DIR.mkdir(exist_ok=True)


CURRENT_DOCUMENT = {
    "filename": None,
    "text": None
}


def render_home(
    request: Request,
    filename=None,
    text_preview=None,
    message=None,
    error=None
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
            "error": error
        }
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render_home(
        request=request,
        filename=CURRENT_DOCUMENT["filename"]
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    """
    Handle PDF upload, save it, extract text, and display preview.
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

        CURRENT_DOCUMENT["filename"] = file.filename
        CURRENT_DOCUMENT["text"] = extracted_text

        return render_home(
            request=request,
            filename=file.filename,
            text_preview=extracted_text[:2000],
            message="PDF uploaded and text extracted successfully."
        )

    except Exception as error:
        return render_home(
            request=request,
            error=str(error)
        )