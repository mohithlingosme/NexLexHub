# NexLexHub Architecture

## Overview

NexLexHub is organized as a legal intelligence stack rather than a publishing stack.

1. Discovery engines collect metadata-only legal events from publisher pages.
2. Official source fetchers normalize judgments, gazette materials, and tribunal sources.
3. Processing modules extract text, metadata, chunks, citations, and embeddings.
4. PostgreSQL stores structured legal entities and pgvector embeddings.
5. FastAPI exposes search, analysis, graph, alert, and AI workspace APIs.
6. Next.js renders a dense workspace UI for research and analysis.

## Backend Modules

- `src/nexlexhub/api/`: FastAPI app, schemas, endpoint wiring
- `src/nexlexhub/core/`: settings, logging, auth, JWT, rate limiting
- `src/nexlexhub/db/`: SQLAlchemy models, engine/session setup, DB types
- `src/nexlexhub/services/`: bootstrap seeding and legal intelligence orchestration
- `src/nexlexhub/rag/`: query expansion, retrieval, reranking, grounding
- `src/nexlexhub/processing/`: PDF, OCR, chunking, citations, embeddings, metadata extraction
- `src/nexlexhub/official_sources/`: source retrieval scaffolds for courts, gazette, tribunals
- `src/nexlexhub/agents/`: extraction, verification, editorial, compliance helpers
- `src/nexlexhub/worker/`: Celery app

## Data Model

Primary tables:

- `users`
- `courts`
- `judges`
- `publishers`
- `cases`
- `judgments`
- `judgment_chunks`
- `citations`
- `precedents`
- `statutes`
- `legal_events`
- `embeddings`
- `alerts`
- `ai_conversations`

Production uses PostgreSQL + pgvector. Tests use SQLite-compatible type variants for JSON/vector fields so the application can self-test without a live container.

## Frontend

The frontend lives in `frontend/app/` and is structured as a workspace shell with dedicated routes for:

- `/`
- `/search`
- `/cases`
- `/graph`
- `/timeline`
- `/workspace`
- `/statutes`
- `/alerts`
- `/settings`
- `/admin`

## Auth Model

- API key RBAC for simple service and dashboard access
- JWT bearer tokens for analyst/admin AI flows
- in-memory rate limiting keyed by API key or JWT subject

## Deployment Shape

- `Dockerfile` boots the API after running Alembic migrations
- `docker-compose.yml` provisions Postgres + pgvector, Redis, API, and worker
- Celery is available for asynchronous ingestion and verification work
