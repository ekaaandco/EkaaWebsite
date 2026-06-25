"""Ekaa — The Event Collective.

A small FastAPI app that serves a wedding planning marketing site.
All visible copy lives in content.yaml so it can be edited without touching code.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import yaml
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
ENQUIRIES_FILE = DATA_DIR / "enquiries.jsonl"

app = FastAPI(title="Ekaa — The Event Collective")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def load_content() -> dict:
    """Read site copy fresh on each request so edits show without a restart."""
    with open(BASE_DIR / "content.yaml", "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def whatsapp_link(content: dict) -> str:
    """Build a click to WhatsApp link prefilled with a friendly opener."""
    phone = content["contact"]["phone_e164"]
    opener = content["contact"].get("whatsapp_opener", "")
    return f"https://wa.me/{phone}?text={quote(opener)}"


def asset_version() -> int:
    """Mtime of the stylesheet, used to bust caches when the CSS changes."""
    try:
        return int((BASE_DIR / "static" / "css" / "style.css").stat().st_mtime)
    except OSError:
        return 0


def base_context(request: Request) -> dict:
    content = load_content()
    return {
        "request": request,
        "c": content,
        "whatsapp": whatsapp_link(content),
        "year": datetime.now().year,
        "v": asset_version(),
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", base_context(request))


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", base_context(request))


@app.get("/book", response_class=HTMLResponse)
async def book(request: Request, sent: bool = False):
    ctx = base_context(request)
    ctx["sent"] = sent
    return templates.TemplateResponse("book.html", ctx)


@app.post("/book")
async def book_submit(
    request: Request,
    name: str = Form(...),
    contact: str = Form(...),
    wedding_when: str = Form(""),
    city: str = Form(""),
    note: str = Form(""),
):
    """Store the enquiry and confirm.

    Enquiries are appended to data/enquiries.jsonl. Wiring this to email
    (ekaaandco@gmail.com) or a form service is a later, low effort step.
    """
    record = {
        "received": datetime.now().isoformat(timespec="seconds"),
        "name": name.strip(),
        "contact": contact.strip(),
        "wedding_when": wedding_when.strip(),
        "city": city.strip(),
        "note": note.strip(),
    }
    with open(ENQUIRIES_FILE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return RedirectResponse(url="/book?sent=true", status_code=303)


@app.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    ctx = base_context(request)
    ctx.update(
        page_title="Privacy policy",
        page_heading="How we handle your details",
        body=[
            "Ekaa is a wedding planning studio based in Mumbai. This page explains "
            "what we do with the information you share with us.",
            "When you send an enquiry, we collect only what you give us: your name, "
            "your phone or email, a rough wedding date, a city, and a short note. We "
            "use these to reply to you and to plan your wedding. Nothing more.",
            "We do not sell your details to anyone. We do not share them beyond the "
            "vendors and team members who need them to deliver your wedding, and only "
            "with your knowledge.",
            "If you would like us to delete your details at any time, write to us and "
            "we will remove them.",
        ],
    )
    return templates.TemplateResponse("legal.html", ctx)


@app.get("/terms", response_class=HTMLResponse)
async def terms(request: Request):
    ctx = base_context(request)
    ctx.update(
        page_title="Terms",
        page_heading="The basics of working together",
        body=[
            "This website is for sharing what Ekaa does and for starting a "
            "conversation. The words and images here are owned by Ekaa and its "
            "photographers and may not be reused without permission.",
            "An enquiry is not a booking. We confirm scope, timelines, and "
            "commercials in a written agreement before any work begins.",
            "These terms will grow as the studio does. For anything not covered here, "
            "the simplest thing is to ask us directly.",
        ],
    )
    return templates.TemplateResponse("legal.html", ctx)


@app.get("/health")
async def health():
    return {"status": "ok"}
