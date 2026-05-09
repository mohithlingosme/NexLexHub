from __future__ import annotations

import os

os.environ.setdefault("NEXLEXHUB_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/nexlexhub")
os.environ.setdefault("NEXLEXHUB_SYNC_DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/nexlexhub")
os.environ.setdefault("NEXLEXHUB_ALLOWED_KEYS", "dev-api-key:admin")
os.environ.setdefault("NEXLEXHUB_ENABLE_DEMO_SEED", "true")
