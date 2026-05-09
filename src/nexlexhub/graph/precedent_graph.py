from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.db.models import Case, Precedent


async def build_precedent_edges(session: AsyncSession) -> list[dict]:
    rows = (await session.execute(select(Precedent, Case).join(Case, Case.id == Precedent.source_case_id))).all()
    return [
        {
            "source_case_id": precedent.source_case_id,
            "source_title": case.title,
            "cited_case_id": precedent.cited_case_id,
            "cited_text": precedent.cited_text,
            "treatment": precedent.treatment,
        }
        for precedent, case in rows
    ]
