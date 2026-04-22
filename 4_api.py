from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger("nexlexhub_api")

app = FastAPI(title="NexLexHub RAG API", version="1.0.0")

here = Path(__file__).resolve().parent
agent_root = here / "ai-legal-news-agent"
if str(agent_root) not in sys.path:
    sys.path.insert(0, str(agent_root))

from ai.rag import answer_with_context_meta, retrieve, store_stats  # noqa: E402


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    k: int = Field(4, ge=1, le=25)
    include_contexts: bool = True


class ContextItem(BaseModel):
    id: Optional[str] = None
    url: str = ""
    title: str = ""
    date: str = ""
    chunk_index: Optional[int] = None
    text: str = ""


class AskResponse(BaseModel):
    answer: str
    used_ollama: bool
    backend: str
    contexts: Optional[List[ContextItem]] = None


@app.get("/health")
def health() -> Dict[str, Any]:
    try:
        stats = store_stats()
        return {"ok": True, "vector_store": stats}
    except FileNotFoundError:
        return {"ok": True, "vector_store": {"loaded": False}}


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest) -> AskResponse:
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="question must be non-empty")

    try:
        stats = store_stats()
        backend = str(stats.get("backend") or "")
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=f"vector store missing: {exc}") from exc

    try:
        ctx = retrieve(question, k=payload.k)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=f"vector store missing: {exc}") from exc
    except Exception as exc:
        logger.exception("Retrieve failed")
        raise HTTPException(status_code=500, detail="retrieve failed") from exc

    try:
        answer, used_ollama = answer_with_context_meta(question, ctx)
    except Exception as exc:
        logger.exception("Answer generation failed")
        raise HTTPException(status_code=500, detail="answer generation failed") from exc

    contexts_out = [ContextItem.model_validate(x) for x in ctx] if payload.include_contexts else None
    return AskResponse(answer=answer, used_ollama=used_ollama, backend=backend, contexts=contexts_out)


# Run: `uvicorn 4_api:app --reload`
