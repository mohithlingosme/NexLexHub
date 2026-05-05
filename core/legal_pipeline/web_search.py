"""Serper web search client for legal context augmentation."""

import httpx
import logging
from typing import List
from pathlib import Path

from core.config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)

SERPER_URL = "https://google.serper.dev/search"
NUM_RESULTS = 5

async def search_case_context(title: str, content_snippet: str = "") -> List[str]:
    """Search Serper for case context: top 5 snippets."""
    api_key = DEFAULT_CONFIG.serper_api_key
    if not api_key:
        logger.warning("SERPER_API_KEY missing, skipping search")
        return []
    
    query = f'"{title}" "Supreme Court" case analysis precedents OR "legal principles" OR "procedural history"'
    if content_snippet:
        query += f' {content_snippet[:100]}'
    
    payload = {
        "q": query,
        "num": NUM_RESULTS,
        "gl": "in",  # India focus
        "lr": "lang_en"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                SERPER_URL,
                json=payload,
                headers={"X-API-KEY": api_key, "Content-Type": "application/json"}
            )
            resp.raise_for_status()
            data = resp.json()
            
            snippets = []
            for result in data.get("organic", [])[:NUM_RESULTS]:
                snippet = result.get("snippet", "")
                if snippet:
                    snippets.append(snippet)
            
            logger.info("Serper search: %d snippets for '%s'", len(snippets), title[:50])
            return snippets
            
    except Exception as e:
        logger.error("Serper search failed: %s", e)
        return []

if __name__ == "__main__":
    import asyncio
    async def test():
        snippets = await search_case_context("Notify all airports Supreme Court Satinder Singh Bhasin")
        print("Snippets:", snippets)
    asyncio.run(test())

