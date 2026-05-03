BEGIN TRANSACTION;
CREATE TABLE legal_blogs (
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
    );
DELETE FROM "sqlite_sequence";
COMMIT;
