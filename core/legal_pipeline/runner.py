"""CLI runner."""

import asyncio
import argparse
import logging
from pathlib import Path

from core.legal_pipeline import process_file
from core.legal_pipeline.types import SupremeCourtCase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    parser = argparse.ArgumentParser("Legal Pipeline Runner")
    parser.add_argument("--input", "-i", required=True, type=Path, help="Input JSON path")
    parser.add_argument("--limit", "-l", type=int, help="Process first N cases")
    parser.add_argument("--output-dir", "-o", type=Path, help="Output dir")
    
    args = parser.parse_args()
    
    if not args.input.exists():
        logger.error("Input not found: %s", args.input)
        return 1
    
    results = await process_file(args.input, args.limit)
    logger.info("Processed %d cases", len(results))
    
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))

