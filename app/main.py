"""FastAPI app.   uvicorn app.main:app --reload"""
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app import pipeline

STATIC = Path(__file__).parent / "static"
app = FastAPI(title="Grounded Support IVA")


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=1000)


class Citation(BaseModel):
    title: str
    url: str
    section: str | None = None


class Handoff(BaseModel):
    summary: str
    intent: str
    articles_tried: list[str]


class ChatResponse(BaseModel):
    status: Literal["answered", "clarify", "out_of_scope", "handoff"]
    answer: str
    citations: list[Citation]
    handoff: Handoff | None = None


@app.on_event("startup")
def warm_up() -> None:
    try:
        from app.embedder import embed
        embed(["warm up"])
    except Exception:
        pass                                   # the first request will load it instead


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


VALID = {"answered", "clarify", "out_of_scope", "handoff"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> dict:
    try:
        out = pipeline.handle(req.session_id, req.message.strip())
        if out.get("status") not in VALID:
            raise ValueError("invalid status")
        return out
    except Exception:
        return {"status": "out_of_scope", "answer": pipeline.FALLBACK, "citations": [], "handoff": None}

@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")