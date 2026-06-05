from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title = "ComplyAI - AI Policy Compliance Assistant")

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "app_name": "ComplyAI",
            "subtitle": "Your AI Policy Compliance Assistant",
            "message":"Upload policy documents, analyze rules, detect risks, and generate compliance outputs."
        }
    )