#!/usr/bin/env python3
"""Indian Kanoon scraper. Note: Rate-limited; use search queries for cases/news."""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List

from playwright.async_api import async_playwright  # type: ignore

from config import DEFAULT_CONFIG

CATEGORY_QUERIES = {
    "case law": "judgment",
    "statutes": "act section",
    "news": "news",
}

DEFAULT_MAX_PAGES = DEFAULT_CONFIG.scraper.max_pages
DEFAULT_OUT_FILE = DEFAULT_CONFIG.paths.raw_articles.replace("articles.json", "indiakanoon_docs.json")


async def scrape(
    *,
    categories: List[str] = ["case law", "statutes"],
    out_file: str = DEFAULT_OUT_FILE,
    max_pages: int = DEFAULT_MAX_PAGES,
) -> List[Dict[str, Any]]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://indiankanoon.org/")
        
        all_docs = []
        for cat in categories:
            query = CATEGORY_QUERIES.get(cat, "law")
            search_url = f"https://indiankanoon.org/search/?formInput={query}"
            await page.goto(search_url)
            
            # Extract docs from search results
            docs = await page.locator(".doc_row").all()
            for doc in docs[:max_pages]:
                title = await doc.locator(".title").text_content()
                url = await doc.locator("a").get_attribute("href")
                full_url = f"https://indiankanoon.org{url}" if url else ""
                all_docs.append({
                    "url": full_url,
                    "title": title,
                    "source": "indiakanoon",
                    "scraped_at": asyncio.get_event_loop().time(),
                })
        
        await browser.close()
        
        Path(out_file).parent.mkdir(exist_ok=True, parents=True)
        Path(out_file).write_text(json.dumps(all_docs, indent=2))
        return all_docs
