from __future__ import annotations

import asyncio
import json

from nexlexhub.scrapers.discovery import BarAndBenchAllahabadHighCourtEngine


async def scrape() -> list[dict]:
    records = await BarAndBenchAllahabadHighCourtEngine().discover()
    return [record.__dict__ for record in records]


if __name__ == "__main__":
    print(json.dumps(asyncio.run(scrape()), indent=2))
