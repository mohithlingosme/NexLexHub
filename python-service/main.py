from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="NexLexHub AI Service", version="0.1.0")


class AnalyzeRequest(BaseModel):
    query: str


class AnalyzeResponse(BaseModel):
    query: str
    intent: str
    answer: str
    retrieval_candidates: List[Dict[str, str]]
    rag_ready: Dict[str, str]


def retrieve_documents(query: str) -> List[Dict[str, str]]:
    """Placeholder for RAG retrieval logic (vector DB / embeddings lookup)."""
    return [
        {"doc_id": "placeholder-1", "title": "Sample Legal Note", "score": "0.00"},
    ]


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    docs = retrieve_documents(payload.query)
    return AnalyzeResponse(
        query=payload.query,
        intent="legal_information_request",
        answer="This is a placeholder structured response. Integrate LLM + retrieval for production.",
        retrieval_candidates=docs,
        rag_ready={
            "embedding_pipeline": "pending",
            "vector_store": "pending",
            "reranker": "pending",
        },
    )
