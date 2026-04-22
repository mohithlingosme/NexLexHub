import asyncio
import logging
from dataclasses import dataclass
from typing import Iterable, Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PipelineConfig:
    max_pages: int = 10


class PipelineRunner:
    """
    Thin orchestration wrapper around the individual pipeline steps.
    Kept separate from `main.py` so you can call the pipeline from other code
    (future API / scheduler / CI).
    """

    def __init__(self, config: Optional[PipelineConfig] = None) -> None:
        self.config = config or PipelineConfig()

    async def scrape(self) -> None:
        from scraper.livelaw_scraper import scrape

        await scrape(max_pages=self.config.max_pages)

    def clean(self) -> None:
        from pipeline.cleaner import clean_articles

        clean_articles()

    def dedup(self) -> None:
        from pipeline.deduplicator import deduplicate_articles

        deduplicate_articles()

    def chunk(self) -> None:
        from pipeline.chunker import chunk_articles

        chunk_articles()

    def summarize(self) -> None:
        from ai.summarize import summarize_articles

        summarize_articles()

    def run_steps(self, steps: Iterable[str], *, strict: bool = True) -> None:
        for step in steps:
            logger.info("Running step: %s", step)
            try:
                if step == "scrape":
                    asyncio.run(self.scrape())
                elif step == "clean":
                    self.clean()
                elif step == "dedup":
                    self.dedup()
                elif step == "chunk":
                    self.chunk()
                elif step == "summarize":
                    self.summarize()
                else:
                    raise ValueError(f"Unknown pipeline step: {step}")
            except Exception:
                logger.exception("Step failed: %s", step)
                if strict:
                    raise

    def run_full(self, *, strict: bool = True) -> None:
        self.run_steps(["scrape", "clean", "dedup", "chunk", "summarize"], strict=strict)

