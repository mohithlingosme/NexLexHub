"""Unit/Integration Tests for Pharse_1 Pipeline.

pytest -v --cov ."""

import pytest
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

from config import config
from cleaner import ingest_bulk, clean_text, compute_hash
from chunker import chunk_smart
from validator import LegalDocument, validate_quality
from sql_exporter import insert_documents, init_db

@pytest.fixture
def sample_html():
    return '<html><body><h1>Test Case</h1><p>Facts: Test facts. Ruling: Test ruling.</p></body></html>'

@pytest.fixture
def sample_doc():
    return {
        'source_hash': 'abc123',
        'source_file': 'test.json',
        'title': 'Unique Test Case v. India',
        'facts': 'Valid facts',
        'confidence_score': 0.85,
        'issues': ['Issue 1'],
        'statutes': ['IPC 420'],
        'final_ruling': 'Dismissed'
    }

def test_clean_text(sample_html):
    cleaned = clean_text(sample_html)
    assert 'Test Case' in cleaned
    assert len(cleaned) > 0

def test_compute_hash():
    h1 = compute_hash('test')
    h2 = compute_hash('test')
    assert h1 == h2
    assert len(h1) == 16

def test_chunk_smart():
    text = 'Sentence one. Sentence two. ' * 1000
    chunks = chunk_smart(text)
    assert len(chunks) > 1
    assert all(len(c) <= 8000 for c in chunks)

def test_legal_document_valid(sample_doc):
    doc = LegalDocument.model_validate(sample_doc)
    assert doc.confidence_score >= config.min_confidence
    assert 'Generic' not in doc.title

def test_legal_document_reject_generic():
    bad_doc = sample_doc.copy()
    bad_doc['title'] = 'Supreme Court Cases'
    with pytest.raises(ValueError):
        LegalDocument.model_validate(bad_doc)

def test_validate_quality(sample_doc):
    assert validate_quality(sample_doc) is True

def test_init_db(tmp_path):
    db_path = tmp_path / 'test.db'
    config.sqlite_db = db_path  # Temp override
    init_db()
    assert db_path.exists()

@patch('Pharse_1.Scraper.Script.sql_exporter.sqlite3.connect')
def test_insert_documents(mock_conn, sample_doc):
    docs = [sample_doc]
    insert_documents(docs)
    mock_conn.execute.assert_called()

def test_ingest_bulk_empty(tmp_path):
    config.raw_dir = tmp_path
    docs = ingest_bulk()
    assert len(docs) == 0

# Integration: End-to-end dry-run stub
@patch('ollama.chat')
def test_pipeline_dry(mock_ollama, sample_doc):
    # Mock ingest/chunk/extract
    with patch('Pharse_1.Scraper.Script.Ai_pipelines.ingest_bulk', return_value=[{'cleaned_content': 'test'}]):
        from Ai_pipelines import PipelineOrchestrator
        orch = PipelineOrchestrator()
        orch.run()
    mock_ollama.assert_called()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

