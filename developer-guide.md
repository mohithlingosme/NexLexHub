# Developer Guide

## Code ownership map

- API: `src/nexlexhub/api/`
- Auth and settings: `src/nexlexhub/core/`
- ORM + sessions: `src/nexlexhub/db/`
- Retrieval pipeline: `src/nexlexhub/rag/`
- Processing pipeline: `src/nexlexhub/processing/`
- Official source retrieval: `src/nexlexhub/official_sources/`
- Discovery engines: `src/nexlexhub/scrapers/`
- Frontend workspace: `frontend/app/`

## Rules

- Keep legacy wrappers under `Pharse_1/` functional; they should delegate into `src/nexlexhub/scrapers`.
- Ship schema changes through `alembic/versions/`.
- Prefer Postgres-compatible types in production, but preserve SQLite compatibility for tests.
- Do not reintroduce SQLite article stores or full publisher-body retention.

## Standard checks

- `pytest -q`
- `python -m ruff check .`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
