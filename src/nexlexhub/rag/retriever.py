from __future__ import annotations

import math
import re
from collections import Counter

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.db.models import Case, Citation, Embedding, JudgmentChunk
from nexlexhub.processing.embedding_pipeline import generate_embedding
from nexlexhub.rag.query_expansion import expand_query
from nexlexhub.rag.reranker import rerank


_WORD_RE = re.compile(r"[a-z0-9]+(?:/[a-z0-9]+)*", re.I)


def _tokenize_legal(s: str) -> list[str]:
    s = (s or "").lower()
    return _WORD_RE.findall(s)


def _bm25_score(query_tokens: list[str], doc_tokens: list[str], *, k1: float = 1.5, b: float = 0.75, avgdl: float = 1.0) -> float:
    # lightweight BM25 approximation (no corpus statistics). Uses avgdl=avg doc length from candidate pool.
    if not query_tokens or not doc_tokens:
        return 0.0
    doc_len = len(doc_tokens)
    denom_factor = k1 * (1 - b + b * (doc_len / (avgdl or 1.0)))
    term_counts = Counter(doc_tokens)
    score = 0.0
    # pseudo idf: boost rare terms within doc using 1/(1+tf)
    for t in set(query_tokens):
        tf = term_counts.get(t, 0)
        if tf <= 0:
            continue
        idf = 1.0 / (1.0 + tf)
        score += idf * ((tf * (k1 + 1)) / (tf + denom_factor))
    return score


async def semantic_retrieve(session: AsyncSession, query: str, limit: int = 5) -> list[dict]:
    """Production-ish hybrid retrieval.

    Pipeline:
      1) BM25-style lexical scoring (client-side, within pgvector candidate pool)
      2) pgvector cosine distance scoring (server-side)
      3) weighted merge + rerank

    Backward compatible return schema: case_id/title/citation/chunk_id/text/score/verified
    """

    query_embedding = generate_embedding(query)

    # --- pgvector candidate pool (server-side) ---
    # We intentionally over-fetch to allow lexical BM25 re-scoring over the candidate pool.
    candidate_limit = max(1, limit * 10)
    stmt = (
        select(
            JudgmentChunk,
            Case,
            (Embedding.vector.cosine_distance(query_embedding)).label("cos_dist"),
        )
        .join(Embedding, Embedding.chunk_id == JudgmentChunk.id)
        .join(Case, Case.id == JudgmentChunk.case_id)
        .order_by(Embedding.vector.cosine_distance(query_embedding).asc())
        .limit(candidate_limit)
    )

    try:
        rows = (await session.execute(stmt)).all()
    except Exception:
        # SQLite/dev fallback: cosine operator may not exist.
        # We'll degrade to an embedding-free lexical retrieval over chunk text.
        # This keeps API/tests working, while pgvector remains production path.
        chunks_stmt = (
            select(JudgmentChunk, Case, JudgmentChunk.id.label("dummy"))
            .join(Case, Case.id == JudgmentChunk.case_id)
            .limit(candidate_limit)
        )
        rows = []
        for chunk, case, _dummy in (await session.execute(chunks_stmt)).all():
            rows.append((chunk, case, 1.0))  # cos_dist neutral-ish


    # --- BM25-like lexical scoring (client-side) over candidates ---
    expanded = expand_query(query)
    # Use first expansion as primary lexical basis.
    query_tokens = _tokenize_legal(expanded[0])

    # compute avg candidate doc length for mild normalization
    candidate_doc_tokens = [
        _tokenize_legal(chunk.text) for (chunk, _case, _cos) in rows
    ]
    avgdl = (sum(len(toks) for toks in candidate_doc_tokens) / (len(candidate_doc_tokens) or 1)) or 1.0

    # weights (tuned conservatively for demo corpus)
    bm25_weight = 0.65
    vec_weight = 0.35

    results: list[dict] = []
    for (chunk, case, cos_dist), doc_tokens in zip(rows, candidate_doc_tokens):
        bm25 = _bm25_score(query_tokens, doc_tokens, avgdl=avgdl)

        # Convert cosine distance to similarity-ish score.
        # cos_dist in [0,2] typical; map to [0,1] with clamp-ish behavior.
        vec_sim = 1.0 - float(cos_dist)
        merged = (bm25_weight * bm25) + (vec_weight * vec_sim)

        results.append(
            {
                "case_id": case.id,
                "title": case.title,
                "citation": case.citation,
                "chunk_id": chunk.id,
                "text": chunk.text,
                "score": round(float(merged), 4),
                "verified": case.official_source_found,
            }
        )

    # rerank with query-aware legal factors
    return rerank(results, query=query)[:limit]




async def fetch_case_citations(session: AsyncSession, case_id: int) -> list[str]:

    rows = (await session.execute(select(Citation.raw_text).where(Citation.case_id == case_id))).scalars().all()
    return list(rows)
