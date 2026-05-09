from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.db.models import Citation


async def build_citation_graph(session: AsyncSession) -> list[dict]:
    rows = (await session.execute(select(Citation))).scalars().all()
    return [
        {
            "case_id": row.case_id,
            "chunk_id": row.chunk_id,
            "citation": row.normalized_text,
            "verified": row.verified,
        }
        for row in rows
    ]
