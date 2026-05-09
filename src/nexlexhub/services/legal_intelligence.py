from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.agents.compliance_agent import evaluate as compliance_evaluate
from nexlexhub.agents.editorial_agent import synthesize
from nexlexhub.agents.verification_agent import verify
from nexlexhub.compliance.attribution_engine import build_attribution
from nexlexhub.db.models import Case, Citation, Court, LegalEvent, Precedent
from nexlexhub.graph.graph_builder import build_graph
from nexlexhub.rag.citation_grounding import ground_answer
from nexlexhub.rag.retriever import fetch_case_citations, semantic_retrieve


async def search_cases(session: AsyncSession, query: str) -> list[Case]:
    stmt = select(Case).where(
        Case.title.ilike(f"%{query}%") | Case.summary.ilike(f"%{query}%") | Case.citation.ilike(f"%{query}%")
    )
    return list((await session.execute(stmt)).scalars().all())


async def timeline(session: AsyncSession) -> list[dict]:
    rows = (
        await session.execute(
            select(Case.title, Case.decision_date, Court.name)
            .join(Court, Court.id == Case.court_id, isouter=True)
            .order_by(Case.decision_date.desc())
        )
    ).all()
    return [{"title": title, "decision_date": str(decision_date), "court": court} for title, decision_date, court in rows]


async def related_cases(session: AsyncSession, case_id: int) -> list[dict]:
    rows = (await session.execute(select(Precedent).where(Precedent.source_case_id == case_id))).scalars().all()
    return [{"cited_case_id": row.cited_case_id, "cited_text": row.cited_text, "treatment": row.treatment} for row in rows]


async def legal_analysis(session: AsyncSession, query: str) -> dict:
    retrieved = await semantic_retrieve(session, query)
    citations = []
    if retrieved:
        citations = await fetch_case_citations(session, retrieved[0]["case_id"])
    answer = synthesize(query, " ".join(item["text"] for item in retrieved[:2]), citations)
    grounded = ground_answer(answer, citations)
    verification = verify(answer, citations)
    compliance = compliance_evaluate(answer, query)
    attribution = build_attribution(
        source_url="https://nexlexhub.local/search",
        publisher="NexLexHub",
        official_source_url=retrieved[0]["citation"] if retrieved else None,
    )
    return {
        "query": query,
        "results": retrieved,
        "grounding": grounded,
        "verification": verification,
        "compliance": compliance,
        "attribution": attribution,
    }


async def citations_index(session: AsyncSession) -> list[dict]:
    rows = (await session.execute(select(Citation))).scalars().all()
    return [{"id": row.id, "citation": row.normalized_text, "verified": row.verified} for row in rows]


async def precedents_index(session: AsyncSession) -> list[dict]:
    rows = (await session.execute(select(Precedent))).scalars().all()
    return [{"id": row.id, "cited_text": row.cited_text, "treatment": row.treatment} for row in rows]


async def summary_counts(session: AsyncSession) -> dict[str, int]:
    case_count = await session.scalar(select(func.count()).select_from(Case)) or 0
    event_count = await session.scalar(select(func.count()).select_from(LegalEvent)) or 0
    return {"cases": case_count, "events": event_count}


async def graph_snapshot(session: AsyncSession) -> dict:
    return await build_graph(session)
