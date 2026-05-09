from __future__ import annotations

from nexlexhub.domain.types import DiscoveryRecord
from nexlexhub.scrapers.discovery import run_all_discovery_engines


async def execute() -> list[DiscoveryRecord]:
    return await run_all_discovery_engines()
