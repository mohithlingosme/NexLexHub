from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Paths:
    raw_articles: str = "data/raw/articles.json"
    clean_articles: str = "data/processed/clean_articles.json"
    dedup_articles: str = "data/processed/deduplicated_articles.json"
    processed_articles: str = "data/processed/processed_articles.json"
    chunks_dir: str = "data/chunks"
    chunks_glob: str = "data/chunks/chunk_*.json"
    vector_store: str = "data/processed/vector_store.json"


@dataclass(frozen=True)
class OllamaConfig:
    base_url: str = "http://localhost:11434"
    summarize_model: str = "llama3"
    embed_model: str = "nomic-embed-text"

    @property
    def generate_url(self) -> str:
        return f"{self.base_url}/api/generate"

    @property
    def embeddings_url(self) -> str:
        return f"{self.base_url}/api/embeddings"

    @property
    def tags_url(self) -> str:
        return f"{self.base_url}/api/tags"


@dataclass(frozen=True)
class ScraperConfig:
    max_pages: int = 10
    concurrency: int = 6
    retries: int = 3
    base_delay_s: float = 1.5
    navigation_timeout_ms: int = 60_000
    page_settle_ms: int = 600
    polite_delay_s: float = 1.2


@dataclass(frozen=True)
class ChunkerConfig:
    max_chars: int = 1200
    overlap: int = 150
    chunks_per_file: int = 200
    purge_existing: bool = True


@dataclass(frozen=True)
class AppConfig:
    paths: Paths = Paths()
    ollama: OllamaConfig = OllamaConfig()
    scraper: ScraperConfig = ScraperConfig()
    chunker: ChunkerConfig = ChunkerConfig()


DEFAULT_CONFIG = AppConfig()

