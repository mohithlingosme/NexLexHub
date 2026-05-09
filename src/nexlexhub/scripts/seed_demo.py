from __future__ import annotations

import asyncio

from nexlexhub.db.session import SessionLocal
from nexlexhub.services.bootstrap import seed_demo_data


async def _run() -> None:
    async with SessionLocal() as session:
        await seed_demo_data(session)


def main() -> None:
    asyncio.run(_run())
