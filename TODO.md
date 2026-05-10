# NexLexHub Migration TODO (Phase 1 -> Production PGVector Legal RAG)

- [ ] Upgrade embedding pipeline to local sentence-transformers (keep hash fallback)
- [ ] Refactor semantic retrieval to use pgvector SQL similarity (server-side)
- [ ] Add hybrid retrieval (BM25 + pgvector) and score fusion
- [ ] Add retrieval reranking integration (ensure compatible scoring fields)
- [ ] Add citation-aware chunking integration with chunk<->citation grounding
- [ ] Ensure /semantic-search and /legal-analysis keep working end-to-end
- [ ] Add safe SQLite->Postgres migration steps via Alembic
- [ ] Update Docker + docker-compose for Postgres+pgvector+model deps
- [ ] Run tests and API smoke checks

