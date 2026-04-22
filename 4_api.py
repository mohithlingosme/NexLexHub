from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

here = Path(__file__).resolve().parent
agent_root = here / "ai-legal-news-agent"
if str(agent_root) not in sys.path:
    sys.path.insert(0, str(agent_root))

from ai.rag import answer_with_context, retrieve  # noqa: E402


class Query(BaseModel):
    question: str = Field(..., min_length=1)
    k: int = Field(4, ge=1, le=25)


@app.post("/ask")
def ask(query: Query):
    ctx = retrieve(query.question, k=query.k)
    answer = answer_with_context(query.question, ctx)
    return {"answer": answer, "contexts": ctx}


# Run: `uvicorn 4_api:app --reload`

