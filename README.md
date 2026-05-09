# NexLexHub

NexLexHub is now a legal intelligence and legal RAG platform. The runtime no longer depends on SQLite article stores or article-rewriting flows. The platform is organized around discovery metadata, official-source retrieval, citation-aware chunking, embeddings, semantic retrieval, knowledge graph views, and compliance-safe analysis.

## Stack

- FastAPI backend
- PostgreSQL + pgvector
- SQLAlchemy ORM + Alembic
- Redis + Celery
- Next.js frontend

## Main capabilities

- Metadata-only legal event discovery
- Official judgment and gazette source normalization
- Citation extraction and precedent linking
- Semantic chunking and embedding generation
- Hybrid retrieval and grounded legal analysis
- Knowledge graph endpoints for cases, citations, courts, and precedents

## Quick start

```bash
copy .env.example .env
pip install -r requirements.txt
docker compose up -d postgres redis
alembic upgrade head
nexlexhub-seed
uvicorn nexlexhub.api.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## API

- `GET /health`
- `POST /search`
- `GET /cases`
- `GET /citations`
- `GET /precedents`
- `POST /semantic-search`
- `POST /legal-analysis`
- `GET /timeline`
- `GET /related-cases/{case_id}`
- `GET /graph`

All protected endpoints require `X-API-Key`.

## Legacy compatibility

The old scraper entrypoints still exist, but they now delegate to the discovery-engine architecture and emit metadata-only event records instead of full article bodies.
