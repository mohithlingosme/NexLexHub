#!/usr/bin/env python3
"""NexLexHub FastAPI server for Phase 1 (RAG + scraping endpoints)."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import uvicorn

from pipeline.processor import PipelineRunner
from ai.rag import answer_with_context_meta
from config import DEFAULT_CONFIG

app = FastAPI(title="NexLexHub API", version="1.0")

class AskRequest(BaseModel):
    question: str
    include_contexts: bool = False

class AskResponse(BaseModel):
    answer: str
    used_ollama: bool
    sources: List[str]

@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    try:
        from ai.rag import retrieve
        contexts = retrieve(request.question, k=4)
        answer, used_ollama = answer_with_context_meta(request.question, contexts)
        return AskResponse(answer=answer, used_ollama=used_ollama, sources=["rag"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape")
async def trigger_scrape(sources: List[str] = ["livelaw", "barbench", "indiakanoon"]):
    runner = PipelineRunner()
    await runner.scrape(sources=sources)
    return {"status": "scraping completed", "sources": sources}

@app.get("/health")
async def health():
    return {"status": "ok", "ollama_available": True}  # Check later

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
