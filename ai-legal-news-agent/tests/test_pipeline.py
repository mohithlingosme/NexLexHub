import unittest
import json
import os
from scraper.livelaw_scraper import scrape
from pipeline.cleaner import main as clean_main
from pipeline.chunker import main as chunk_main
from ai.summarize import main as summarize_main
from utils.file_utils import load_json

class TestPipeline(unittest.TestCase):
    def test_cleaner_output(self):
        clean_main()
        articles = load_json("data/processed/clean_articles.json")
        self.assertGreater(len(articles), 0)
        self.assertIn("title", articles[0])
    
    def test_chunker_output(self):
        chunk_main()
        self.assertTrue(os.path.exists("data/chunks/chunk_0.json"))

if __name__ == '__main__':
    unittest.main()

