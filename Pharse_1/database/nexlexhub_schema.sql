-- NexLexHub Pharse_1 Production Schema
-- SQLite + MySQL/MariaDB compatible

-- Core legal documents table
CREATE TABLE IF NOT EXISTS legal_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_hash TEXT UNIQUE NOT NULL,
    source_file TEXT NOT NULL,
    source_url TEXT,
    case_type TEXT,
    court_name TEXT,
    bench TEXT,
    judges TEXT,  -- JSON array
    decision_date TEXT,
    citation_reference TEXT,
    jurisdiction TEXT,
    title TEXT NOT NULL,
    facts TEXT,
    procedural_history TEXT,
    issues TEXT,  -- JSON array
    findings TEXT,
    statutes TEXT,  -- JSON array
    precedents TEXT,  -- JSON array
    final_ruling TEXT,
    legal_significance TEXT,
    seo_keywords TEXT,  -- JSON array
    seo_summary TEXT,
    industry_domain TEXT,
    document_type TEXT,
    confidence_score REAL,
    qa_pass BOOLEAN DEFAULT 0,
    processing_version TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Automotive (future Autopredator)
CREATE TABLE IF NOT EXISTS automotive_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_hash TEXT UNIQUE NOT NULL,
    source_file TEXT NOT NULL,
    oem_specs TEXT,
    variant_details TEXT,
    pricing TEXT,
    regulatory_notices TEXT,
    siam_reports TEXT,
    dealer_data TEXT,  -- JSON
    insurance TEXT,
    finance TEXT,
    confidence_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit trail
CREATE TABLE IF NOT EXISTS processing_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    model_name TEXT,
    docs_processed INTEGER,
    failures INTEGER,
    avg_confidence REAL,
    total_time REAL,  -- seconds
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Failed ingestions (resume safety)
CREATE TABLE IF NOT EXISTS failed_ingestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    source_hash TEXT,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Source registry (dedup + provenance)
CREATE TABLE IF NOT EXISTS source_registry (
    source_hash TEXT PRIMARY KEY,
    source_file TEXT NOT NULL,
    file_size INTEGER,
    word_count INTEGER,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_processed TIMESTAMP,
    status TEXT DEFAULT 'pending'  -- pending|processed|failed
);

-- Model runs (fine-tuning tracking)
CREATE TABLE IF NOT EXISTS model_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    run_id TEXT NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    avg_confidence REAL,
    hallucination_rate REAL,
    qa_pass_rate REAL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_legal_source_hash ON legal_documents(source_hash);
CREATE INDEX IF NOT EXISTS idx_legal_confidence ON legal_documents(confidence_score);
CREATE INDEX IF NOT EXISTS idx_legal_court ON legal_documents(court_name);
CREATE INDEX IF NOT EXISTS idx_source_status ON source_registry(status);

-- Insert schema version
INSERT OR IGNORE INTO processing_logs (run_id, model_name, docs_processed) 
VALUES ('schema_init', 'v1.0', 0);

-- MySQL-specific triggers (auto-update timestamp)
DELIMITER //
CREATE TRIGGER IF NOT EXISTS update_legal_timestamp 
BEFORE UPDATE ON legal_documents 
FOR EACH ROW 
SET NEW.updated_at = CURRENT_TIMESTAMP//
DELIMITER ;

