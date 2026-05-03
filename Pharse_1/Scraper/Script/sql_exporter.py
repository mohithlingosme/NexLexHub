"""SQL Exporter: SQLite upsert + MySQL dump generation."""

import sqlite3
import json
from pathlib import Path
from typing import List
from datetime import datetime

from config import config
from .validator import LegalDocument

logger = logging.getLogger(__name__)

def init_db():
    """Apply schema if missing."""
    conn = sqlite3.connect(config.sqlite_db)
with open(str(Path(__file__).parent.parent.parent / 'database/nexlexhub_schema.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    logger.info(f'DB ready: {config.sqlite_db}')

def insert_documents(docs: List[Dict]):
    """Upsert LegalDocuments to SQLite."""
    init_db()
    conn = sqlite3.connect(config.sqlite_db)
    
    for doc_dict in docs:
        try:
            # Validate first
            doc = LegalDocument.model_validate(doc_dict)
            doc_json = doc.model_dump_json()
            
            conn.execute('''
                INSERT OR REPLACE INTO legal_documents (
                    source_hash, source_file, source_url, court_name, title, facts,
                    procedural_history, issues, findings, statutes, precedents,
                    final_ruling, legal_significance, confidence_score, judges
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                doc.source_hash, doc.source_file, doc.source_url, doc.court_name,
                doc.title, doc.facts, doc.procedural_history, json.dumps(doc.issues),
                doc.findings, json.dumps(doc.statutes), json.dumps(doc.precedents),
                doc.final_ruling, doc.legal_significance, doc.confidence_score,
                json.dumps(doc.judges)
            ))
        except Exception as e:
            logger.error(f'SQL insert failed {doc_dict.get("source_hash")}: {e}')
    
    conn.commit()
    conn.close()
    logger.info(f'Inserted {len(docs)} docs to SQLite')

def export_mysql_dump():
    """Dump SQLite to MySQL-compatible SQL."""
    dump_path = config.output_dir / 'nexlexhub_mysql_dump.sql'
    conn = sqlite3.connect(config.sqlite_db)
    
    with open(dump_path, 'w') as f:
        for line in conn.iterdump():
            f.write(line + '\n')
    
    logger.info(f'MySQL dump: {dump_path}')
    return dump_path

if __name__ == '__main__':
    print('SQL Exporter CLI - use via pipeline')

