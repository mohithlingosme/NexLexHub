#!/usr/bin/env python3
import argparse
import logging
import sys
from scraper.livelaw_scraper import scrape
from pipeline.cleaner import main as clean
from pipeline.deduplicator import main as dedup
from pipeline.chunker import main as chunk
from ai.summarize import main as summarize

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="AI Legal News Pipeline")
    parser.add_argument('step', choices=['scrape', 'clean', 'dedup', 'chunk', 'summarize', 'all'], 
                        help='Pipeline step to run')
    args = parser.parse_args()
    
    try:
        if args.step == 'all' or args.step == 'scrape':
            logger.info("🕷️  Scraping...")
            asyncio.run(scrape())
        
        if args.step == 'all' or args.step == 'clean':
            logger.info("🧹 Cleaning...")
            clean()
        
        if args.step == 'all' or args.step == 'dedup':
            logger.info("🔄 Deduplicating...")
            dedup()
        
        if args.step == 'all' or args.step == 'chunk':
            logger.info("📦 Chunking...")
            chunk()
        
        if args.step == 'all' or args.step == 'summarize':
            logger.info("🤖 AI Summarizing...")
            summarize()
            
        logger.info("✅ Pipeline complete!")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    main()

