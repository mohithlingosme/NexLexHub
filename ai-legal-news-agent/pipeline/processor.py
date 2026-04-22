import asyncio
import logging
from dataclasses import dataclass, replace
from typing import Iterable, Optional, Sequence

from config import DEFAULT_CONFIG, AppConfig

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PipelineConfig:
    max_pages: int = DEFAULT_CONFIG.scraper.max_pages
    scrape_timeout_s: int = 300
    with_embeddings: bool = False


class PipelineRunner:
    """
    Thin orchestration wrapper around the individual pipeline steps.
    Kept separate from `main.py` so you can call the pipeline from other code
    (future API / scheduler / CI).
    """

    def __init__(self, config: Optional[PipelineConfig] = None, *, app_config: AppConfig = DEFAULT_CONFIG) -> None:
        self.config = config or PipelineConfig()
        self.app_config = app_config

    async def scrape(self) -> None:
        from scraper.livelaw_scraper import scrape

        cfg = replace(self.app_config, scraper=replace(self.app_config.scraper, max_pages=self.config.max_pages))
        if self.config.scrape_timeout_s and self.config.scrape_timeout_s > 0:
            await asyncio.wait_for(scrape(max_pages=cfg.scraper.max_pages), timeout=self.config.scrape_timeout_s)
        else:
            await scrape(max_pages=cfg.scraper.max_pages)

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

    def embed(self) -> None:
        from ai.embed import build_vector_store

        build_vector_store()

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
                elif step == "embed":
                    self.embed()
                else:
                    raise ValueError(f"Unknown pipeline step: {step}")
            except Exception:
                logger.exception("Step failed: %s", step)
                if strict:
                    raise

    def run_full(self, *, strict: bool = True, with_embeddings: Optional[bool] = None) -> None:
        steps: Sequence[str] = ["scrape", "clean", "dedup", "chunk", "summarize"]
        want_embed = self.config.with_embeddings if with_embeddings is None else bool(with_embeddings)
        if want_embed:
            steps = list(steps) + ["embed"]
        self.run_steps(steps, strict=strict)
