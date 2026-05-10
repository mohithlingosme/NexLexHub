from __future__ import annotations

import os
from pathlib import Path

import pytest


DB_PATH = Path(".pytest_nexlexhub.db").resolve()
os.environ["NEXLEXHUB_DATABASE_URL"] = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"
os.environ["NEXLEXHUB_SYNC_DATABASE_URL"] = f"sqlite:///{DB_PATH.as_posix()}"
os.environ["NEXLEXHUB_ALLOWED_KEYS"] = "dev-api-key:admin"
os.environ["NEXLEXHUB_ENABLE_DEMO_SEED"] = "false"
os.environ["NEXLEXHUB_AUTO_INIT_DB"] = "true"

from nexlexhub.db.base import Base  # noqa: E402
from nexlexhub.db.session import engine  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    if DB_PATH.exists():
        DB_PATH.unlink()
