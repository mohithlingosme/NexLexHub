from __future__ import annotations

import asyncio
import hashlib
import logging
import re
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from aiohttp import ClientTimeout

import aiohttp
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed

from nexlexhub.core.config import get_settings
from nexlexhub.domain.types import DiscoveryRecord

logger = logging.getLogger(__name__)


class DiscoveryEngine:
    publisher = ""
    topic_urls: list[str] = []
    court = ""
    include_path = ""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._robots_cache: dict[str, RobotFileParser] = {}
        self._delay = 0.5

    async def _robots(self, base_url: str) -> RobotFileParser:
        if base_url in self._robots_cache:
            return self._robots_cache[base_url]
        parser = RobotFileParser()
        parser.set_url(urljoin(base_url, "/robots.txt"))
        parser.read()
        self._robots_cache[base_url] = parser
        return parser

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def _fetch(self, session: aiohttp.ClientSession, url: str) -> str:
        await asyncio.sleep(self._delay)
        timeout = ClientTimeout(total=30)
        async with session.get(url, headers={"User-Agent": self.settings.user_agent}, timeout=timeout) as response:
            response.raise_for_status()
            if response.status >= 400:
                raise RuntimeError(f"bad status {response.status}")
            return await response.text()

    def _valid_article(self, url: str) -> bool:
        return self.include_path in urlparse(url).path.lower() and "/topic/" not in url

    def _entities(self, headline: str) -> list[str]:
        return sorted(set(re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", headline)))

    async def discover(self) -> list[DiscoveryRecord]:
        records: list[DiscoveryRecord] = []
        async with aiohttp.ClientSession() as session:
            for topic_url in self.topic_urls:
                base_url = f"{urlparse(topic_url).scheme}://{urlparse(topic_url).netloc}"
                robots = await self._robots(base_url)
                if not robots.can_fetch(self.settings.user_agent, topic_url):
                    logger.info("robots_disallow", extra={"url": topic_url, "publisher": self.publisher})
                    continue
                html = await self._fetch(session, topic_url)
                soup = BeautifulSoup(html, "html.parser")
                seen: set[str] = set()
                for anchor in soup.select("a[href]"):
                    raw_href = anchor.get("href")
                    if not isinstance(raw_href, str):
                        continue
                    href = urljoin(base_url, raw_href)
                    headline = " ".join(anchor.get_text(" ", strip=True).split())
                    if not headline or href in seen or not self._valid_article(href):
                        continue
                    seen.add(href)
                    records.append(
                        DiscoveryRecord(
                            headline=headline[:500],
                            publisher=self.publisher,
                            source_url=href,
                            publish_date=datetime.now(timezone.utc).isoformat(),
                            court=self.court,
                            snippet=headline[:240],
                            entities=self._entities(headline),
                            official_source_found=False,
                            event_hash=hashlib.sha256(f"{self.publisher}|{href}|{headline}".encode("utf-8")).hexdigest(),
                        )
                    )
        clustered: dict[str, DiscoveryRecord] = {}
        for record in records:
            key = re.sub(r"[^a-z0-9]+", "-", record.headline.lower()).strip("-")
            clustered.setdefault(key, record)
        return list(clustered.values())


class LiveLawSupremeCourtEngine(DiscoveryEngine):
    publisher = "LiveLaw"
    topic_urls = ["https://www.livelaw.in/supreme-court"]
    court = "Supreme Court"
    include_path = "/supreme-court"


class BarAndBenchSupremeCourtEngine(DiscoveryEngine):
    publisher = "BarAndBench"
    topic_urls = ["https://www.barandbench.com/topic/supreme-court-of-india"]
    court = "Supreme Court"
    include_path = "/news/"


class LiveLawKarnatakaHighCourtEngine(DiscoveryEngine):
    publisher = "LiveLaw"
    topic_urls = ["https://www.livelaw.in/high-court/karnataka-high-court"]
    court = "Karnataka High Court"
    include_path = "/high-court/karnataka-high-court"


class BarAndBenchAllahabadHighCourtEngine(DiscoveryEngine):
    publisher = "BarAndBench"
    topic_urls = ["https://www.barandbench.com/topic/allahabad-high-court"]
    court = "Allahabad High Court"
    include_path = "/news/"


async def run_all_discovery_engines() -> list[DiscoveryRecord]:
    engines = [
        LiveLawSupremeCourtEngine(),
        BarAndBenchSupremeCourtEngine(),
        LiveLawKarnatakaHighCourtEngine(),
        BarAndBenchAllahabadHighCourtEngine(),
    ]
    results = await asyncio.gather(*(engine.discover() for engine in engines))
    return [item for batch in results for item in batch]
