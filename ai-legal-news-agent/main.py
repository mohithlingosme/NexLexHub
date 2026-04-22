#!/usr/bin/env python3
import argparse
import asyncio
import logging
import os
import sys
from typing import Optional

logger = logging.getLogger("ai_legal_news_agent")


def _configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _ensure_local_imports() -> None:
    """
    Make `ai/`, `pipeline/`, etc importable even when running `python` from
    a different working directory.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    if here and here not in sys.path:
        sys.path.insert(0, here)


async def run_scrape(max_pages: int, *, timeout_s: int) -> None:
    from scraper.livelaw_scraper import scrape

    if timeout_s and timeout_s > 0:
        await asyncio.wait_for(scrape(max_pages=max_pages), timeout=timeout_s)
    else:
        await scrape(max_pages=max_pages)


def run_clean() -> None:
    from pipeline.cleaner import clean_articles

    clean_articles()


def run_dedup() -> None:
    from pipeline.deduplicator import deduplicate_articles

    deduplicate_articles()


def run_chunk() -> None:
    from pipeline.chunker import chunk_articles

    chunk_articles()


def run_summarize() -> None:
    from ai.summarize import summarize_articles

    summarize_articles()


def main(argv: Optional[list[str]] = None) -> int:
    _ensure_local_imports()

    parser = argparse.ArgumentParser(description="AI Legal News Agent pipeline")
    parser.add_argument(
        "step",
        choices=["scrape", "clean", "dedup", "chunk", "summarize", "full", "all"],
        help="Pipeline step to run (use 'full' for end-to-end)",
    )
    parser.add_argument("--max-pages", type=int, default=10, help="Max pages per category to scrape")
    parser.add_argument(
        "--scrape-timeout-s",
        type=int,
        default=300,
        help="Global timeout for scraping during 'full' (0 disables)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail fast instead of continuing when a step errors during 'full'",
    )
    args = parser.parse_args(argv)

    _configure_logging(verbose=args.verbose)

    step = "full" if args.step == "all" else args.step

    try:
        if step in ("full", "scrape"):
            logger.info("Step: scrape")
            try:
                asyncio.run(run_scrape(max_pages=args.max_pages, timeout_s=args.scrape_timeout_s))
            except Exception:
                logger.exception("Scrape step failed.")
                if step != "full" or args.strict:
                    raise
        if step in ("full", "clean"):
            logger.info("Step: clean")
            try:
                run_clean()
            except Exception:
                logger.exception("Clean step failed.")
                if step != "full" or args.strict:
                    raise
        if step in ("full", "dedup"):
            logger.info("Step: dedup")
            try:
                run_dedup()
            except Exception:
                logger.exception("Dedup step failed.")
                if step != "full" or args.strict:
                    raise
        if step in ("full", "chunk"):
            logger.info("Step: chunk")
            try:
                run_chunk()
            except Exception:
                logger.exception("Chunk step failed.")
                if step != "full" or args.strict:
                    raise
        if step in ("full", "summarize"):
            logger.info("Step: summarize")
            try:
                run_summarize()
            except Exception:
                logger.exception("Summarize step failed.")
                if step != "full" or args.strict:
                    raise

        logger.info("Pipeline complete.")
        return 0
    except KeyboardInterrupt:
        logger.warning("Interrupted.")
        return 130
    except Exception:
        logger.exception("Pipeline failed.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
