import os
import re
import json
import time
import sqlite3
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from slugify import slugify
from tqdm import tqdm
from bs4 import BeautifulSoup
import ollama
from pydantic import BaseModel, Field, ValidationError


# =========================================
# CONFIG
# =========================================
MODEL_NAME = "llama3.1"
INPUT_FOLDER = "Pharse_1\Scraper\Data\Structured\Structured_SC_Blogs.json"
DB_FILE = "nexlexhub_processed.db"
SQL_DUMP_FILE = "nexlexhub_processed.sql"
FAILED_LOG_FILE = "failed_logs.json"
PROCESS_LOG = "ai_pipeline.log"

MAX_RETRIES = 4
BATCH_SIZE = 20
TEMPERATURE = 0
TOP_P = 0.1
NUM_PREDICT = 7000
REPEAT_PENALTY = 1.2
MAX_CHUNK_SIZE = 12000


# =========================================
# LOGGING
# =========================================
logging.basicConfig(
    filename=PROCESS_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================================
# PYDANTIC SCHEMA
# =========================================
class LegalBlogSchema(BaseModel):
    title: str = Field(
        description="Exact case-specific SEO title"
    )
    introduction: str
    facts: str
    procedural_history: str
    issues: List[str]
    findings: str
    principles: List[str]
    statutes: List[str]
    precedents: List[str]
    final_ruling: str
    significance: str
    confidence_score: float


# =========================================
# DATABASE INIT
# =========================================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
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
    return conn


# =========================================
# FILE CLEANING
# =========================================
def clean_text(raw_text):
    raw_text = re.sub(r'\s+', ' ', raw_text)
    raw_text = re.sub(r'[^\x00-\x7F]+', ' ', raw_text)
    return raw_text.strip()


def extract_html_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ")


# =========================================
# FILE READER
# =========================================
def read_file(file_path):
    ext = Path(file_path).suffix.lower()

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:
            content = f.read()

        if ext == ".html":
            content = extract_html_text(content)

        elif ext == ".json":
            content = json.dumps(
                json.loads(content),
                indent=2
            )

        return clean_text(content)

    except Exception as e:
        logging.error(
            f"Failed reading file {file_path}: {e}"
        )
        return None


# =========================================
# HASHING
# =========================================
def generate_hash(content):
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


# =========================================
# CHUNKING
# =========================================
def chunk_text(text, max_size=MAX_CHUNK_SIZE):
    return [
        text[i:i + max_size]
        for i in range(0, len(text), max_size)
    ]


# =========================================
# PROMPT ENGINEERING
# =========================================
def build_prompt(raw_text):
    return f"""
You are an elite Supreme Court legal editor,
judicial analyst, and legal intelligence engine.

TASK:
Extract ONLY source-specific legal intelligence.

STRICT RULES:
- Output ONLY valid JSON
- Follow schema EXACTLY
- Use ONLY source material
- NO generic summaries
- NO broad court descriptions
- NO fabricated facts
- NO hallucinated precedents
- NO invented statutes
- Exact title
- Exact facts
- Exact procedural history
- Exact issues
- Exact statutes
- Exact precedents
- Exact findings
- Exact final ruling
- Exact legal significance
- SEO-grade legal article quality
- Law student digest style
- If unavailable:
  "Information not sufficiently available"

QUALITY RULE:
Generic titles like:
"Supreme Court Cases"
"Court Judgment"
"Legal Summary"
ARE INVALID.

JSON SCHEMA:
{json.dumps(LegalBlogSchema.model_json_schema(), indent=2)}

SOURCE:
{raw_text}
"""


# =========================================
# OLLAMA EXTRACTION
# =========================================
def extract_blog_data(raw_text):
    prompt = build_prompt(raw_text)

    for attempt in range(MAX_RETRIES):
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a legal research "
                            "and judicial publishing engine."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                format=LegalBlogSchema.model_json_schema(),
                options={
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "repeat_penalty": REPEAT_PENALTY,
                    "num_predict": NUM_PREDICT
                }
            )

            parsed = LegalBlogSchema.model_validate_json(
                response["message"]["content"]
            )

            return parsed.model_dump()

        except Exception as e:
            logging.warning(
                f"Ollama retry {attempt+1} failed: {e}"
            )
            time.sleep(3)

    raise RuntimeError(
        "Ollama extraction failed after retries."
    )


# =========================================
# QUALITY VALIDATION
# =========================================
def validate_blog_quality(blog):
    banned_titles = [
        "Supreme Court Cases",
        "Court Judgment",
        "Legal Summary",
        "Supreme Court"
    ]

    if blog["title"].strip() in banned_titles:
        return False

    if len(blog["issues"]) < 1:
        return False

    if len(blog["principles"]) < 2:
        return False

    if len(blog["statutes"]) < 1:
        return False

    if blog["confidence_score"] < 0.65:
        return False

    return True


# =========================================
# SQL INSERT
# =========================================
def insert_blog(conn, source_hash, source_file, blog):
    slug = slugify(blog["title"])

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
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        source_hash,
        source_file,
        blog["title"],
        slug,
        blog["introduction"],
        blog["facts"],
        blog["procedural_history"],
        json.dumps(blog["issues"]),
        blog["findings"],
        json.dumps(blog["principles"]),
        json.dumps(blog["statutes"]),
        json.dumps(blog["precedents"]),
        blog["final_ruling"],
        blog["significance"],
        blog["confidence_score"],
        datetime.now().isoformat()
    ))


# =========================================
# SQL EXPORT
# =========================================
def export_sql_dump():
    conn = sqlite3.connect(DB_FILE)

    with open(
        SQL_DUMP_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")

    conn.close()


# =========================================
# MAIN BULK PROCESSOR
# =========================================
def process_bulk():
    start_time = time.time()

    conn = init_db()
    failed_logs = []

    all_files = []

    for root, _, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.lower().endswith(
                (".txt", ".md", ".json", ".html")
            ):
                all_files.append(
                    os.path.join(root, file)
                )

    logging.info(
        f"Discovered {len(all_files)} source files."
    )

    batch_counter = 0
    processed_count = 0

    for file_path in tqdm(all_files):
        try:
            raw_text = read_file(file_path)

            if not raw_text:
                continue

            source_hash = generate_hash(raw_text)

            existing = conn.execute(
                "SELECT id FROM legal_blogs WHERE source_hash=?",
                (source_hash,)
            ).fetchone()

            if existing:
                continue

            chunks = chunk_text(raw_text)

            combined_results = []

            for chunk in chunks:
                result = extract_blog_data(chunk)

                if validate_blog_quality(result):
                    combined_results.append(result)

            if not combined_results:
                failed_logs.append({
                    "file": file_path,
                    "reason": "Validation failed"
                })
                continue

            # Use highest confidence chunk
            best_blog = max(
                combined_results,
                key=lambda x: x["confidence_score"]
            )

            insert_blog(
                conn,
                source_hash,
                file_path,
                best_blog
            )

            processed_count += 1
            batch_counter += 1

            if batch_counter % BATCH_SIZE == 0:
                conn.commit()

        except Exception as e:
            failed_logs.append({
                "file": file_path,
                "reason": str(e)
            })

    conn.commit()
    conn.close()

    # Failed logs
    with open(
        FAILED_LOG_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            failed_logs,
            f,
            indent=4
        )

    # SQL dump
    export_sql_dump()

    elapsed = round(
        time.time() - start_time,
        2
    )

    print(
        f"SUCCESS: Processed {processed_count} blogs "
        f"in {elapsed} seconds."
    )

    logging.info(
        f"Completed processing {processed_count} blogs "
        f"in {elapsed} seconds."
    )


# =========================================
# EXECUTION
# =========================================
if __name__ == "__main__":
    process_bulk()
