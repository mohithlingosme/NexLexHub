"""Scrapers for legal news sources.

Multi-source dispatcher.
"""

from typing import List, Dict, Any
from config import DEFAULT_CONFIG

async def scrape_sources(sources: List[str] = None, **kwargs) -> List[Dict[str, Any]]:
    """Dispatch to specific scrapers."""
    sources = sources or list(DEFAULT_CONFIG.sources.sources.keys())
    all_articles = []
    for source in sources:
        if source == "livelaw":
            from .livelaw_scraper import scrape as livelaw_scrape
            all_articles.extend(await livelaw_scrape(**kwargs))
        elif source == "barbench":
            from .barbench_scraper import scrape as barbench_scrape
            all_articles.extend(await barbench_scrape(**kwargs))
        elif source == "indiakanoon":
            from .indiakanoon_scraper import scrape as ik_scrape
            all_articles.extend(await ik_scrape(**kwargs))
    return all_articles

