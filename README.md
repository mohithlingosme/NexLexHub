# NexLexHub

NexLexHub is a legal intelligence platform built around official-source retrieval, citation-aware RAG, semantic case search, and a workspace-style frontend. The legacy Phase 1 scraper wrappers remain in place, but the active platform now runs on FastAPI, PostgreSQL/pgvector, Redis/Celery, and Next.js.

## Runtime

- Backend: `src/nexlexhub/api/main.py`
- ORM + schema: `src/nexlexhub/db/models.py`, `alembic/versions/`
- Retrieval: `src/nexlexhub/rag/`
- Processing: `src/nexlexhub/processing/`
- Discovery engines: `src/nexlexhub/scrapers/discovery.py`
- Official source fetchers: `src/nexlexhub/official_sources/`
- Frontend workspace: `frontend/app/`

## Features

- PostgreSQL-first schema for users, cases, judgments, chunks, citations, precedents, statutes, legal events, embeddings, alerts, and AI conversations
- pgvector-ready embeddings with SQLite-compatible test fallback
- Metadata-only discovery records with entity extraction, event hashes, robots checks, retry handling, and clustering
- Citation-aware retrieval and grounded legal analysis endpoints
- JWT login plus API-key access with RBAC and rate limiting
- Streaming AI workspace endpoint at `POST /ai/chat`
- Workspace pages for dashboard, semantic search, case explorer, citation graph, timeline, statutes, alerts, settings, and admin views

## Quick Start

```bash
copy .env.example .env
pip install -r requirements.txt
docker compose up -d postgres redis
alembic upgrade head
uvicorn nexlexhub.api.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Demo credentials:

- `admin@nexlexhub.local` / `admin123`
- `analyst@nexlexhub.local` / `analyst123`

## API Surface

- `GET /health`
- `POST /auth/login`
- `POST /search`
- `POST /semantic-search`
- `GET /cases`
- `GET /citations`
- `GET /precedents`
- `GET /statutes`
- `GET /timeline`
- `POST /legal-analysis`
- `POST /ai/chat`
- `GET /ai/conversations`
- `GET /alerts`
- `GET /graph`

`X-API-Key` supports simple access for reader/admin flows. `Bearer` JWTs are available through `/auth/login` for analyst/admin AI endpoints.

## Verification

Validated in this repo with:

- `pytest -q`
- `python -m ruff check .`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
- `docker compose up -d postgres redis`
- `alembic upgrade head`
- `uvicorn nexlexhub.api.main:app` health + auth + streaming checks
