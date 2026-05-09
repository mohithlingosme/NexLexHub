from functools import lru_cache
from typing import Dict

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NEXLEXHUB_", env_file=".env", extra="ignore")

    app_name: str = "NexLexHub"
    env: str = "dev"
    api_key: str = "dev-api-key"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/nexlexhub"
    sync_database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/nexlexhub"
    redis_url: str = "redis://localhost:6379/0"
    allowed_keys: str = "dev-api-key:admin"
    embedding_provider: str = "hash"
    embedding_dimension: int = 16
    rate_limit_per_minute: int = 120
    enable_demo_seed: bool = True
    log_level: str = "INFO"
    official_source_dir: str = "data/official_sources"
    discovery_output_dir: str = "data/discovery"
    user_agent: str = "NexLexHubBot/2.0 (+https://example.invalid/legal-intelligence)"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    def key_roles(self) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        for item in self.allowed_keys.split(","):
            if ":" not in item:
                continue
            key, role = item.split(":", 1)
            mapping[key.strip()] = role.strip()
        return mapping


@lru_cache
def get_settings() -> Settings:
    return Settings()
