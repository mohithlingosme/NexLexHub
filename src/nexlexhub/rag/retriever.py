from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.db.models import Case, Citation, Embedding, JudgmentChunk
from nexlexhub.processing.embedding_pipeline import generate_embedding
from nexlexhub.rag.query_expansion import expand_query
from nexlexhub.rag.reranker import rerank


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


async def semantic_retrieve(session: AsyncSession, query: str, limit: int = 5) -> list[dict]:
    query_embedding = generate_embedding(query)
    rows = (
        await session.execute(
            select(JudgmentChunk, Embedding, Case)
            .join(Embedding, Embedding.chunk_id == JudgmentChunk.id)
            .join(Case, Case.id == JudgmentChunk.case_id)
        )
    ).all()
    results = []
    expanded = expand_query(query)
    for chunk, embedding, case in rows:
        bm25_hint = sum(1 for token in expanded[0].lower().split() if token in chunk.text.lower())
        score = float(_dot(query_embedding, embedding.vector) + (0.05 * bm25_hint))
        results.append(
            {
                "case_id": case.id,
                "title": case.title,
                "citation": case.citation,
                "chunk_id": chunk.id,
                "text": chunk.text,
                "score": round(score, 4),
                "verified": case.official_source_found,
            }
        )
    return rerank(results)[:limit]


async def fetch_case_citations(session: AsyncSession, case_id: int) -> list[str]:
    rows = (await session.execute(select(Citation.raw_text).where(Citation.case_id == case_id))).scalars().all()
    return list(rows)
