import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.chunker import chunk_articles
from pipeline.cleaner import clean_articles
from pipeline.deduplicator import deduplicate_articles
from utils.file_utils import load_json, save_json


class TestPipeline(unittest.TestCase):
    def test_clean_dedup_chunk_smoke(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            raw = root / "raw.json"
            cleaned = root / "clean.json"
            deduped = root / "dedup.json"
            chunks_dir = root / "chunks"

            save_json(
                [
                    {
                        "title": "Valid Article",
                        "content": "A" * 250,
                        "date": "2026-04-22T00:00:00Z",
                        "url": "https://example.com/x-1",
                    },
                    {"title": "Too Short", "content": "short", "date": "2026-04-22", "url": "x"},
                    {"title": "", "content": "B" * 300, "date": "2026-04-22", "url": "y"},
                    {
                        "title": "MCQ",
                        "content": "Question 1) ... MCQ ... " + ("C" * 400),
                        "date": "2026-04-22",
                        "url": "z",
                    },
                ],
                raw,
            )

            cleaned_items = clean_articles(input_file=str(raw), output_file=str(cleaned), min_chars=200)
            self.assertEqual(len(cleaned_items), 1)
            self.assertEqual(cleaned_items[0]["title"], "Valid Article")

            # Add a duplicate and ensure dedup removes it.
            save_json(cleaned_items + [cleaned_items[0]], cleaned)
            dedup_items = deduplicate_articles(input_file=str(cleaned), output_file=str(deduped))
            self.assertEqual(len(dedup_items), 1)

            paths = chunk_articles(
                input_file=str(deduped),
                output_dir=str(chunks_dir),
                max_chars=120,
                overlap=10,
                chunks_per_file=50,
            )
            self.assertTrue(paths)
            for p in paths:
                self.assertTrue(Path(p).exists())

            chunk0 = load_json(paths[0], default=[])
            self.assertIsInstance(chunk0, list)
            self.assertTrue(chunk0)
            self.assertIn("text", chunk0[0])
            self.assertLessEqual(len(chunk0[0]["text"]), 120)


if __name__ == "__main__":
    unittest.main()

