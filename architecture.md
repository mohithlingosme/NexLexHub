# NexLexHub Architecture

NexLexHub now centers on legal intelligence primitives:

- Discovery engines collect event metadata only.
- Official source fetchers resolve judgments, gazette materials, and tribunal sources.
- Processing modules extract metadata, chunks, embeddings, and citations.
- PostgreSQL with pgvector stores structured legal objects and vectors.
- FastAPI serves authenticated search, semantic retrieval, citation, precedent, graph, and analysis endpoints.
- Next.js renders a legal intelligence UI rather than article pages.
- Celery and Redis support asynchronous ingestion and verification tasks.

Core runtime paths:

- Backend: `src/nexlexhub/api/main.py`
- ORM models: `src/nexlexhub/db/models.py`
- Retrieval: `src/nexlexhub/rag/`
- Scrapers: `src/nexlexhub/scrapers/discovery.py`
- Official sources: `src/nexlexhub/official_sources/`
- Frontend: `frontend/`
