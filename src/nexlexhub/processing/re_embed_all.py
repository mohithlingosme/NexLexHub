"""Re-embed all existing JudgmentChunk rows using the configured embedding provider.

This script is intended to be run after the pgvector dimension migration.
It updates Embedding.vector for all chunks.

Usage:
  python -m nexlexhub.processing.re_embed_all

Environment:
  Uses NEXLEXHUB_database_url and NEXLEXHUB_embedding_provider / embedding_model.
"""

from __future__ import annotations

import asyncio
from typing import Iterable

from sqlalchemy import select

from nexlexhub.db.models import Embedding, JudgmentChunk
from nexlexhub.db.session import SessionLocal
from nexlexhub.processing.embedding_pipeline import generate_embedding


async def _iter_chunks(batch_size: int = 256) -> Iterable[JudgmentChunk]:
    offset = 0
    async with SessionLocal() as session:
        while True:
            rows = (await session.execute(select(JudgmentChunk).order_by(JudgmentChunk.id).offset(offset).limit(batch_size))).scalars().all()
            if not rows:
                break
            for row in rows:
                yield row
            offset += batch_size


async def reembed_all() -> None:
    async with SessionLocal() as session:
        chunks = (await session.execute(select(JudgmentChunk).order_by(JudgmentChunk.id))).scalars().all()
        if not chunks:
            return

        updated = 0
        for chunk in chunks:
            # Ensure an Embedding row exists
            emb = await session.scalar(select(Embedding).where(Embedding.chunk_id == chunk.id))
            if emb is None:
                emb = Embedding(chunk_id=chunk.id, provider="local", vector=generate_embedding(chunk.text), bm25_hint=0.0)
                session.add(emb)
                await session.flush()

            # Always update vector to match current embedding model/dimension
            emb.vector = generate_embedding(chunk.text)
            emb.provider = "local"

            emb.bm25_hint = emb.bm25_hint or 0.0
            updated += 1

        await session.commit()
        print(f"Re-embedded {updated} chunks")


def main() -> None:
    asyncio.run(reembed_all())


if __name__ == "__main__":
    main()

