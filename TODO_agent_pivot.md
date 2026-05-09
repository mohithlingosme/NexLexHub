# NexLexHub TODO Roadmap
> Goal: Transform NexLexHub from a scraper-based legal news prototype into a production-grade AI-powered legal intelligence platform.

---

# CURRENT STATUS

## Existing Infrastructure
- [x] Async Playwright scrapers
- [x] Bar & Bench scraper
- [x] LiveLaw scraper
- [x] Deduplication engine
- [x] JSON-LD extraction
- [x] Ollama integration
- [x] Pydantic validation
- [x] SQLite ingestion pipeline
- [x] Structured legal intelligence schema
- [x] Corpus generation

---

# CRITICAL ARCHITECTURAL PIVOT

## REMOVE / REDUCE
- [ ] Full article body storage
- [ ] AI rewritten journalism
- [ ] Long-term publisher content retention
- [ ] Publisher-style article reconstruction

## REPLACE WITH
- [ ] Metadata indexing
- [ ] Official judgment retrieval
- [ ] Legal intelligence extraction
- [ ] Citation-aware processing
- [ ] Semantic legal retrieval

---

# PHASE 1 — REBUILD DATA PIPELINE

## Scraper Refactor
- [ ] Convert scrapers into modular source adapters
- [ ] Create unified scraper interface
- [ ] Add source priority ranking
- [ ] Add robots.txt compliance checks
- [ ] Add adaptive rate limiting
- [ ] Add proxy rotation layer
- [ ] Add scraper health monitoring
- [ ] Add automatic retry queue
- [ ] Add dead-link detection
- [ ] Add anti-duplicate fingerprinting

## Metadata-Only Storage
Store ONLY:
- [ ] headline
- [ ] publisher
- [ ] source_url
- [ ] publish_date
- [ ] author
- [ ] snippet
- [ ] extracted_entities

DO NOT STORE:
- [ ] full article bodies
- [ ] complete publisher content

---

# PHASE 2 — OFFICIAL SOURCE RETRIEVAL

## Supreme Court Integration
- [ ] Supreme Court judgment fetcher
- [ ] Supreme Court PDF parser
- [ ] Citation extraction engine
- [ ] Cause-list tracking
- [ ] Daily judgment watcher

## High Court Integration
- [ ] Karnataka HC
- [ ] Delhi HC
- [ ] Bombay HC
- [ ] Allahabad HC
- [ ] Madras HC

## Government Sources
- [ ] Gazette integration
- [ ] India Code ingestion
- [ ] RBI notifications
- [ ] MCA circulars
- [ ] SEBI orders
- [ ] tribunal orders

---

# PHASE 3 — DOCUMENT PROCESSING ENGINE

## PDF Processing
- [ ] OCR pipeline
- [ ] scanned PDF detection
- [ ] multilingual OCR
- [ ] PDF cleanup pipeline
- [ ] page segmentation
- [ ] layout-aware parsing

## Chunking Engine
- [ ] semantic chunking
- [ ] citation-aware chunking
- [ ] paragraph chunking
- [ ] section tagging
- [ ] heading extraction
- [ ] overlap optimization

## Metadata Extraction
Extract:
- [ ] case number
- [ ] bench
- [ ] judge names
- [ ] court
- [ ] statute references
- [ ] precedent citations
- [ ] timeline events
- [ ] parties
- [ ] advocates

---

# PHASE 4 — LEGAL INTELLIGENCE ENGINE

## Schema Expansion
- [ ] ratio decidendi
- [ ] obiter dicta
- [ ] legal questions
- [ ] procedural posture
- [ ] constitutional provisions
- [ ] jurisdiction
- [ ] outcome classification
- [ ] legal domain classification

## AI Extraction Improvements
- [ ] chunk-based extraction
- [ ] multi-pass extraction
- [ ] validation pipeline
- [ ] hallucination detection
- [ ] confidence scoring
- [ ] source-grounded extraction
- [ ] repair pass pipeline

## Citation Engine
- [ ] pinpoint citations
- [ ] paragraph references
- [ ] case citation parser
- [ ] statute citation parser
- [ ] citation normalization

---

# PHASE 5 — VECTOR SEARCH + RAG

## Database Migration
- [ ] migrate SQLite → PostgreSQL
- [ ] add pgvector
- [ ] schema normalization
- [ ] indexing optimization

## Embeddings
- [ ] bge-large integration
- [ ] jina embeddings
- [ ] embedding cache
- [ ] embedding versioning
- [ ] multilingual embeddings

## Retrieval System
- [ ] semantic search
- [ ] hybrid BM25 + vector retrieval
- [ ] citation-aware retrieval
- [ ] reranking pipeline
- [ ] context compression

## RAG Pipeline
- [ ] query decomposition
- [ ] retrieval orchestration
- [ ] source grounding
- [ ] answer verification
- [ ] citation injection

---

# PHASE 6 — LEGAL KNOWLEDGE GRAPH

## Entity Graph
Build relationships:
- [ ] Case ↔ Judge
- [ ] Case ↔ Statute
- [ ] Case ↔ Precedent
- [ ] Judge ↔ Court
- [ ] Statute ↔ Section
- [ ] Case ↔ Legal Principle

## Graph Features
- [ ] precedent chains
- [ ] judge analytics
- [ ] statute analytics
- [ ] timeline graph
- [ ] legal topic graph
- [ ] citation graph

---

# PHASE 7 — AI NEWSROOM

## Discovery Agent
- [ ] breaking legal news detection
- [ ] trend detection
- [ ] duplicate event clustering
- [ ] importance scoring

## Verification Agent
- [ ] cross-source verification
- [ ] official-source verification
- [ ] citation validation
- [ ] fake-news detection

## Editorial Agent
Generate:
- [ ] legal intelligence briefs
- [ ] judgment explainers
- [ ] procedural summaries
- [ ] legal impact analysis
- [ ] precedent summaries

## Compliance Agent
- [ ] copyright similarity checks
- [ ] publisher overlap detection
- [ ] legal-risk scoring
- [ ] attribution verification

---

# PHASE 8 — FRONTEND + API

## Backend
- [ ] FastAPI migration
- [ ] REST API
- [ ] GraphQL layer
- [ ] authentication
- [ ] RBAC
- [ ] rate limiting

## Frontend
- [ ] Next.js frontend
- [ ] semantic search UI
- [ ] legal research dashboard
- [ ] citation explorer
- [ ] timeline viewer
- [ ] precedent explorer

## Public Features
- [ ] AI legal assistant
- [ ] legal research copilot
- [ ] legal alerts
- [ ] bookmarking
- [ ] saved research folders

---

# PHASE 9 — AUTOMATION + DEVOPS

## Infrastructure
- [ ] Dockerization
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment
- [ ] Redis queues
- [ ] Celery workers
- [ ] monitoring stack

## Observability
- [ ] structured logging
- [ ] scraper monitoring
- [ ] AI cost monitoring
- [ ] hallucination tracking
- [ ] performance metrics

## Security
- [ ] API authentication
- [ ] secrets management
- [ ] encryption
- [ ] audit logs
- [ ] abuse prevention

---

# PHASE 10 — LEGAL SAFETY FRAMEWORK

## Compliance
- [ ] attribution enforcement
- [ ] publisher source linking
- [ ] robots.txt checks
- [ ] paywall detection
- [ ] content minimization

## Safe Publishing Rules
Always:
- [ ] cite official sources
- [ ] link publishers
- [ ] add independent analysis
- [ ] publish transformative output

Never:
- [ ] republish full articles
- [ ] bypass paywalls
- [ ] mirror publisher structure
- [ ] reconstruct journalism

---

# FUTURE FEATURES

## Advanced Legal AI
- [ ] contract analysis
- [ ] compliance assistant
- [ ] litigation strategy engine
- [ ] legal drafting copilot
- [ ] argument generation
- [ ] hearing prediction

## Analytics
- [ ] judge analytics
- [ ] court delay analytics
- [ ] precedent influence scoring
- [ ] litigation trend analysis

## Enterprise
- [ ] law firm dashboard
- [ ] corporate legal ops
- [ ] internal legal knowledge base
- [ ] compliance automation

---

# IMMEDIATE PRIORITIES (NEXT 30 DAYS)

## Highest Priority
- [ ] Stop storing full article bodies
- [ ] Move to PostgreSQL
- [ ] Add pgvector
- [ ] Build official judgment retrieval
- [ ] Implement chunking pipeline
- [ ] Add semantic search
- [ ] Add citation grounding
- [ ] Create metadata-only news ingestion
- [ ] Add legal source verification
- [ ] Build FastAPI backend

---

# LONG-TERM VISION

NexLexHub should evolve into:

"AI-powered legal intelligence and research infrastructure for India"

NOT:

"AI legal news rewriting platform"