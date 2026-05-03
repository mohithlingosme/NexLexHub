"""Production Config for NexLexHub Pharse_1 Pipeline."""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent.resolve()  # Pharse_1/Scraper/Data/Script -> Pharse_1
RAW_DIR = BASE_DIR / 'Scraper/Data/Raw'
PROCESSED_DIR = BASE_DIR / 'Scraper/Data/Processed'
OUTPUT_DIR = BASE_DIR / 'Scraper/Data/Output'
DB_DIR = BASE_DIR / 'database'

# Auto-create dirs
for d in [RAW_DIR, PROCESSED_DIR, OUTPUT_DIR, DB_DIR]:
    d.mkdir(parents=True, exist_ok=True)

@dataclass
class ProcessingConfig:
    """Full production config with .env overrides."""
    
    # Paths (dynamic resolution)
    raw_dir: Path = RAW_DIR
    processed_dir: Path = PROCESSED_DIR
    output_dir: Path = OUTPUT_DIR
    sqlite_db: Path = DB_DIR / 'nexlexhub.db'
    mysql_host: str = os.getenv('MYSQL_HOST', 'localhost')
    mysql_port: int = int(os.getenv('MYSQL_PORT', '3306'))
    mysql_user: str = os.getenv('MYSQL_USER', 'root')
    mysql_password: str = os.getenv('MYSQL_PASSWORD', '')
    mysql_database: str = os.getenv('MYSQL_DATABASE', 'nexlexhub')
    
    # Ollama
    model_name: str = os.getenv('OLLAMA_MODEL', 'qwen2.5')  # or llama3.1
    temperature: float = 0.0
    top_p: float = 0.1
    repeat_penalty: float = 1.2
    num_predict: int = 8000
    
    # Processing
    batch_size: int = int(os.getenv('BATCH_SIZE', '20'))
    max_chunk_size: int = 8000
    max_retries: int = 3
    min_confidence: float = 0.7
    banned_titles: List[str] = field(default_factory=lambda: [
        'Supreme Court Cases', 'Court Judgment', 'Legal Summary', 'Supreme Court'
    ])
    
    # Logging/Metrics
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    preserve_raw: bool = True  # Never delete originals
    
    @classmethod
    def from_env(cls) -> 'ProcessingConfig':
        """Load from .env."""
        return cls()

config = ProcessingConfig.from_env()

