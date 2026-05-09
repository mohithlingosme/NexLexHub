from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.db.models import Case, Court, Judge
from nexlexhub.graph.citation_graph import build_citation_graph
from nexlexhub.graph.precedent_graph import build_precedent_edges


async def build_graph(session: AsyncSession) -> dict[str, list[dict]]:
    cases = (await session.execute(select(Case))).scalars().all()
    courts = (await session.execute(select(Court))).scalars().all()
    judges = (await session.execute(select(Judge))).scalars().all()
    return {
        "cases": [{"id": c.id, "title": c.title, "court_id": c.court_id} for c in cases],
        "courts": [{"id": c.id, "name": c.name, "level": c.level} for c in courts],
        "judges": [{"id": j.id, "name": j.name, "court_id": j.court_id} for j in judges],
        "precedents": await build_precedent_edges(session),
        "citations": await build_citation_graph(session),
    }
