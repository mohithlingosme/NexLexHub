#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from typing import Optional

from config import DEFAULT_CONFIG
from pipeline.processor import PipelineConfig, PipelineRunner

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


def main(argv: Optional[list[str]] = None) -> int:
    _ensure_local_imports()

    parser = argparse.ArgumentParser(description="AI Legal News Agent pipeline")
    parser.add_argument(
        "step",
        choices=["scrape", "clean", "dedup", "chunk", "summarize", "embed", "full", "all"],
        help="Pipeline step to run (use 'full' for end-to-end)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_CONFIG.scraper.max_pages,
        help="Max pages per category to scrape",
    )
    parser.add_argument(
        "--scrape-timeout-s",
        type=int,
        default=300,
        help="Global timeout for scraping during 'full' (0 disables)",
    )
    parser.add_argument(
        "--with-embeddings",
        action="store_true",
        help="Run embedding/index build after 'full' completes",
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
    runner = PipelineRunner(
        PipelineConfig(
            max_pages=args.max_pages,
            scrape_timeout_s=args.scrape_timeout_s,
            with_embeddings=args.with_embeddings,
        )
    )

    try:
        if step == "full":
            try:
                runner.run_full(strict=args.strict)
            except Exception:
                logger.exception("Pipeline failed.")
                raise
        else:
            runner.run_steps([step], strict=True)

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
