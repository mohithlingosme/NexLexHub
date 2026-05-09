"""
=========================================================
NEXLEXHUB - LEGAL INTELLIGENCE PIPELINE (PRODUCTION SAFE)
=========================================================

FEATURES
--------
✔ Robust SQLite handling
✔ Automatic schema creation
✔ Ollama JSON extraction
✔ Pydantic validation with defaults
✔ Retry-safe inserts
✔ Detailed logging
✔ Duplicate prevention using SHA256
✔ HTML-safe content
✔ Graceful AI failure handling
✔ Malformed JSON recovery
✔ Batch corpus processing
✔ Slug generation
✔ Progress bar support

REQUIREMENTS
------------
pip install ollama pydantic python-slugify tqdm

OLLAMA MODEL
-------------
ollama pull llama3

RUN
---
python main.py
"""

# =========================================================
# IMPORTS
# =========================================================

import os
import json
import sqlite3
import logging
import hashlib
import html
from pathlib import Path
from datetime import datetime
from typing import List

import ollama
from pydantic import BaseModel, ValidationError, Field
from slugify import slugify
from tqdm import tqdm


# =========================================================
# CONFIG
# =========================================================

INPUT_JSON = r"C:\Users\mohit\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Filter\Supreme_Court\Final_training_corpus.json"

DATABASE_FILE = "legal_intelligence.db"

OLLAMA_MODEL = "llama3"

LOG_FILE = "pipeline.log"


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# =========================================================
# PYDANTIC MODEL
# =========================================================

class LegalIntelligence(BaseModel):
    title: str = ""
    introduction: str = ""
    facts: str = ""
    procedural_history: str = ""
    issues: List[str] = Field(default_factory=list)
    findings: str = ""
    principles: List[str] = Field(default_factory=list)
    statutes: List[str] = Field(default_factory=list)
    precedents: List[str] = Field(default_factory=list)
    final_ruling: str = ""
    significance: str = ""
    confidence_score: float = 0.0


# =========================================================
# DATABASE
# =========================================================

def init_db(db_file: str):

    Path(db_file).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_file)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS legal_blogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        source_hash TEXT UNIQUE,
        source_file TEXT,

        title TEXT,
        slug TEXT,

        introduction TEXT,
        facts TEXT,
        procedural_history TEXT,

        issues TEXT,

        findings TEXT,

        principles TEXT,
        statutes TEXT,
        precedents TEXT,

        final_ruling TEXT,
        significance TEXT,

        confidence_score REAL,

        created_at TEXT
    )
    """)

    conn.commit()

    logger.info("Database initialized.")

    return conn


# =========================================================
# HASHING
# =========================================================

def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# =========================================================
# SAFE JSON EXTRACTION
# =========================================================

def extract_json(text: str):

    try:
        return json.loads(text)

    except Exception:

        # Try extracting JSON block
        try:
            start = text.find("{")
            end = text.rfind("}") + 1

            if start != -1 and end != -1:
                extracted = text[start:end]
                return json.loads(extracted)

        except Exception:
            pass

    return None


# =========================================================
# OLLAMA ANALYSIS
# =========================================================

def analyze_case(case_text: str):

    prompt = f"""
You are an advanced legal intelligence engine.

Analyze the following legal judgment and return ONLY VALID JSON.

STRICT RULES:
- Return ONLY JSON
- No markdown
- No explanation
- No commentary
- Ensure all fields exist
- confidence_score must be float between 0 and 1

FORMAT:
{{
    "title": "",
    "introduction": "",
    "facts": "",
    "procedural_history": "",
    "issues": [],
    "findings": "",
    "principles": [],
    "statutes": [],
    "precedents": [],
    "final_ruling": "",
    "significance": "",
    "confidence_score": 0.0
}}

CASE:
{case_text[:12000]}
"""

    try:

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"]

        parsed = extract_json(content)

        if not parsed:
            logger.error("Failed to parse JSON from Ollama.")
            return None

        try:
            validated = LegalIntelligence(**parsed)
            return validated

        except ValidationError as e:
            logger.error(f"Pydantic Validation Error: {e}")
            return None

    except Exception as e:
        logger.exception(f"Ollama Error: {e}")
        return None


# =========================================================
# DATABASE INSERT
# =========================================================

def insert_to_legal_blogs(
    conn,
    intel: LegalIntelligence,
    source_hash: str,
    source_file: str
):

    try:

        conn.execute("""
        INSERT OR IGNORE INTO legal_blogs (

            source_hash,
            source_file,

            title,
            slug,

            introduction,
            facts,
            procedural_history,

            issues,

            findings,

            principles,
            statutes,
            precedents,

            final_ruling,
            significance,

            confidence_score,
            created_at

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            source_hash,
            source_file,

            html.escape(intel.title),
            slugify(intel.title or "untitled"),

            html.escape(intel.introduction),
            html.escape(intel.facts),
            html.escape(intel.procedural_history),

            json.dumps(intel.issues, ensure_ascii=False),

            html.escape(intel.findings),

            json.dumps(intel.principles, ensure_ascii=False),
            json.dumps(intel.statutes, ensure_ascii=False),
            json.dumps(intel.precedents, ensure_ascii=False),

            html.escape(intel.final_ruling),
            html.escape(intel.significance),

            float(intel.confidence_score),

            datetime.now().isoformat()
        ))

        conn.commit()

        if conn.total_changes > 0:
            logger.info(f"Inserted: {intel.title}")
        else:
            logger.warning(f"Duplicate skipped: {intel.title}")

    except sqlite3.Error as e:
        logger.exception(f"SQLite Error: {e}")

    except Exception as e:
        logger.exception(f"Insert Error: {e}")


# =========================================================
# LOAD CORPUS
# =========================================================

def load_corpus(file_path: str):

    try:

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.info(f"Loaded corpus with {len(data)} entries.")

        return data

    except Exception as e:
        logger.exception(f"Failed to load corpus: {e}")
        return []


# =========================================================
# EXTRACT TEXT
# =========================================================

def get_case_text(entry):

    if isinstance(entry, dict):

        for key in [
            "text",
            "content",
            "judgment",
            "document",
            "case_text"
        ]:

            if key in entry:
                return str(entry[key])

    return str(entry)


# =========================================================
# MAIN PIPELINE
# =========================================================

def main():

    logger.info("=" * 60)
    logger.info("NEXLEXHUB LEGAL PIPELINE STARTED")
    logger.info("=" * 60)

    conn = init_db(DATABASE_FILE)

    corpus = load_corpus(INPUT_JSON)

    if not corpus:
        logger.error("Corpus empty.")
        return

    success = 0
    failed = 0

    for idx, entry in enumerate(tqdm(corpus)):

        try:

            case_text = get_case_text(entry)

            if not case_text.strip():
                logger.warning(f"Skipping empty entry {idx}")
                continue

            source_hash = generate_hash(case_text)

            intel = analyze_case(case_text)

            if not intel:
                failed += 1
                continue

            insert_to_legal_blogs(
                conn=conn,
                intel=intel,
                source_hash=source_hash,
                source_file=INPUT_JSON
            )

            success += 1

        except Exception as e:
            logger.exception(f"Pipeline Error at entry {idx}: {e}")
            failed += 1

    conn.close()

    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETED")
    logger.info(f"Success: {success}")
    logger.info(f"Failed : {failed}")
    logger.info("=" * 60)


# =========================================================
# ENTRY
# =========================================================

if __name__ == "__main__":
    main()