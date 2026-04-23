from __future__ import annotations

import os
from dataclasses import dataclass


def _env_int(name: str, default: int, *, min_value: int | None = None, max_value: int | None = None) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        value = default
    else:
        try:
            value = int(raw.strip())
        except ValueError:
            value = default

    if min_value is not None:
        value = max(min_value, value)
    if max_value is not None:
        value = min(max_value, value)
    return value


def _env_float(name: str, default: float, *, min_value: float | None = None, max_value: float | None = None) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        value = default
    else:
        try:
            value = float(raw.strip())
        except ValueError:
            value = default

    if min_value is not None:
        value = max(min_value, value)
    if max_value is not None:
        value = min(max_value, value)
    return value


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
    base_url: str = os.getenv("OLLAMA_BASE_URL") or os.getenv("OLLAMA_HOST") or "http://localhost:11434"
    summarize_model: str = os.getenv("OLLAMA_SUMMARIZE_MODEL") or "llama3"
    embed_model: str = os.getenv("OLLAMA_EMBED_MODEL") or "nomic-embed-text"
    generate_timeout_s: int = _env_int("OLLAMA_GENERATE_TIMEOUT_S", 120, min_value=5, max_value=600)
    embed_timeout_s: int = _env_int("OLLAMA_EMBED_TIMEOUT_S", 120, min_value=5, max_value=600)
    retries: int = _env_int("OLLAMA_RETRIES", 2, min_value=1, max_value=8)
    base_delay_s: float = _env_float("OLLAMA_BASE_DELAY_S", 1.2, min_value=0.1, max_value=30.0)

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
    max_pages: int = _env_int("SCRAPER_MAX_PAGES", 10, min_value=1, max_value=200)
    concurrency: int = _env_int("SCRAPER_CONCURRENCY", 6, min_value=1, max_value=32)
    retries: int = _env_int("SCRAPER_RETRIES", 3, min_value=1, max_value=10)
    base_delay_s: float = _env_float("SCRAPER_BASE_DELAY_S", 1.5, min_value=0.1, max_value=60.0)
    navigation_timeout_ms: int = _env_int("SCRAPER_NAV_TIMEOUT_MS", 60_000, min_value=5_000, max_value=300_000)
    page_settle_ms: int = _env_int("SCRAPER_PAGE_SETTLE_MS", 600, min_value=0, max_value=10_000)
    polite_delay_s: float = _env_float("SCRAPER_POLITE_DELAY_S", 1.2, min_value=0.0, max_value=10.0)
    user_agent: str = os.getenv(
        "SCRAPER_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    )


@dataclass(frozen=True)
class ChunkerConfig:
    max_chars: int = 1200
    overlap: int = 150
    chunks_per_file: int = 200
    purge_existing: bool = True


@dataclass(frozen=True)
class ScraperSources:
    sources: Dict[str, str] = {
        "livelaw": "livelaw_scraper.scrape",
        "barbench": "barbench_scraper.scrape",
        "indiakanoon": "indiakanoon_scraper.scrape",
    }


@dataclass(frozen=True)
class AppConfig:
    paths: Paths = Paths()
    ollama: OllamaConfig = OllamaConfig()
    scraper: ScraperConfig = ScraperConfig()
    chunker: ChunkerConfig = ChunkerConfig()
    sources: ScraperSources = ScraperSources()


DEFAULT_CONFIG = AppConfig()
