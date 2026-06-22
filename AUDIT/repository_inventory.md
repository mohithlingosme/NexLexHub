# PHASE 1: Repository Inventory Audit
**NexLexHub - Complete System Analysis**  
*Generated: 2026-06-22*

---

## 1. PROJECT OVERVIEW

**Repository:** `mohithlingosme/NexLexHub`  
**Description:** A legal system for complete analysis and building personal brand in law  
**Primary Language:** Python (79.2%)  
**Other Languages:** HTML (9.8%), TypeScript (5.4%), PHP (3.1%), JavaScript (1.3%), CSS (0.8%)  
**Repository Size:** 165 MB  
**Last Push:** 2026-05-10  
**License:** None  
**Public:** Yes  
**Status:** Active Development  

---

## 2. DIRECTORY STRUCTURE

```
NexLexHub/
├── .github/                          # GitHub workflows (empty)
├── .graphify/                        # Graph visualization utilities
├── Assets/
│   └── ai-legal-news-agent/          # Phase 1 news scraping pipeline
├── Pharse_1/                         # Phase 1 legacy implementations
├── alembic/                          # Database migrations
│   ├── versions/                     # Migration files (3 total)
│   ├── env.py
│   └── script.py.mako
├── frontend/                         # Next.js React frontend
│   ├── app/                          # Next.js app directory
│   │   ├── admin/
│   │   ├── alerts/
│   │   ├── cases/
│   │   ├── graph/
│   │   ├── search/
│   │   ├── settings/
│   │   ├── statutes/
│   │   ├── timeline/
│   │   ├── workspace/
│   │   ├── data.ts
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── workspace-shell.tsx
│   │   └── globals.css
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.ts
│   ├── next-env.d.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── postcss.config.js
├── production/                       # Production deployment files (empty)
├── python-service/                   # Standalone Python API service
├── src/
│   └── nexlexhub/
│       ├── agents/                   # LLM-powered agents
│       │   ├── compliance_agent.py
│       │   ├── discovery_agent.py
│       │   ├── editorial_agent.py
│       │   ├── extraction_agent.py
│       │   └── verification_agent.py
│       ├── api/                      # FastAPI endpoints
│       │   ├── main.py
│       │   └── schemas.py
│       ├── compliance/               # Compliance & attribution
│       │   ├── attribution_engine.py
│       │   ├── copyright_checker.py
│       │   └── source_similarity.py
│       ├── core/                     # Configuration & security
│       │   ├── config.py
│       │   ├── security.py
│       │   └── logging.py
│       ├── db/                       # Database layer
│       │   ├── base.py
│       │   ├── models.py
│       │   ├── session.py
│       │   └── types.py
│       ├── domain/                   # Domain models (empty)
│       ├── graph/                    # Graph building utilities (empty)
│       ├── official_sources/         # Official source fetchers (empty)
│       ├── processing/               # Data processing pipeline
│       │   ├── chunker.py
│       │   ├── citation_extractor.py
│       │   ├── embedding_pipeline.py
│       │   ├── metadata_extractor.py
│       │   ├── ocr_pipeline.py
│       │   ├── pdf_processor.py
│       │   └── re_embed_all.py
│       ├── rag/                      # Retrieval-Augmented Generation
│       │   ├── citation_grounding.py
│       │   ├── query_expansion.py
│       │   ├── reranker.py
│       │   └── retriever.py
│       ├── scrapers/                 # Data scrapers (empty)
│       ├── scripts/                  # CLI utilities
│       │   └── seed_demo.py (inferred)
│       ├── services/                 # Business logic
│       │   ├── bootstrap.py
│       │   └── legal_intelligence.py
│       ├── worker/                   # Celery async tasks
│       │   └── celery_app.py
│       └── __init__.py
├── tests/                            # Test suite (empty)
├── tools/                            # Utility tools (empty)
├── .env.example                      # Environment template
├── .gitignore
├── .gitkeep
├── alembic.ini                       # Alembic configuration
├── architecture.md                   # Architecture documentation
├── articles.json                     # Sample articles data
├── config.php                        # Legacy PHP config
├── deployment-guide.md               # Deployment instructions
├── developer-guide.md                # Developer guide
├── Dockerfile                        # Docker container definition
├── docker-compose.yml                # Docker Compose setup
├── failed_logs.json                  # Debug logs
├── final_blog_output.json            # Sample output
├── final_blog_output.md              # Sample markdown
├── GRAPH.md                          # Graph documentation
├── GRAPH_test.md                     # Graph test documentation
├── legal_intelligence.db             # SQLite dev database
├── livelaw_supremecourt.db           # Sample data database
├── ML_planning.md                    # ML planning document
├── nexlexhub_processed.db            # Processed data database
├── nexlexhub_processed.sql           # SQL schema
├── PROJECT_CODE_ATLAS.md             # Code structure documentation
├── PROJECT_CODE_INDEX.md             # Code index
├── pyproject.toml                    # Python project configuration
├── README.md                         # Main readme
├── requirements.txt                  # Pip requirements (uses pyproject.toml)
├── setup-guide.md                    # Setup instructions
├── supreme_court_articles.json       # Empty articles file
├── TODO.md                           # General TODO
├── TODO_agent_pivot.md               # Agent TODO
├── TODO_fix.md                       # Fixes TODO
└── TODO_structure_fix.md             # Structure fixes TODO
```

---

## 3. FRAMEWORKS & TECHNOLOGIES

### Backend Stack
| Component | Technology | Version | Status |
|-----------|-----------|---------|--------|
| **API Framework** | FastAPI | 0.115.0+ | ✅ Active |
| **ASGI Server** | Uvicorn | 0.30.6+ | ✅ Active |
| **ORM** | SQLAlchemy | 2.0.36+ | ✅ Active |
| **Migration Tool** | Alembic | 1.13.2+ | ✅ Active |
| **Async Driver** | asyncpg | 0.30.0+ | ✅ Active |
| **Validation** | Pydantic | 2.9.2+ | ✅ Active |
| **Task Queue** | Celery | 5.4.0+ | ✅ Active |
| **Broker** | Redis | 5.1.1+ | ✅ Active |
| **Vector DB** | pgvector | 0.3.5+ | ✅ Active |
| **PDF Processing** | PyPDF | 5.1.0+ | ✅ Active |
| **Web Scraping** | BeautifulSoup4 | 4.12.3+ | ✅ Active |
| **Async HTTP** | aiohttp, httpx | 3.10.10+, 0.27.2+ | ✅ Active |

### Frontend Stack
| Component | Technology | Version | Status |
|-----------|-----------|---------|--------|
| **Framework** | Next.js | 16.2.6 | ✅ Active |
| **Runtime** | React | 19.2.0 | ✅ Active |
| **Styling** | Tailwind CSS | 3.4.14+ | ✅ Active |
| **Language** | TypeScript | 5.6.3+ | ✅ Active |
| **PostCSS** | PostCSS | 8.4.47+ | ✅ Active |

### Database Stack
| Component | Technology | Version | Status |
|-----------|-----------|---------|--------|
| **Primary DB** | PostgreSQL | 16 (pgvector) | ✅ Active |
| **Vector Extension** | pgvector | Latest | ✅ Active |
| **Sync Driver** | psycopg | 3.2.3+ | ✅ Active |
| **Test DB** | SQLite | Built-in | ✅ Active |
| **Caching** | Redis | 7+ | ✅ Active |

### Development Tools
| Tool | Purpose | Status |
|------|---------|--------|
| **Ruff** | Linting | ✅ Configured |
| **MyPy** | Type Checking | ✅ Configured |
| **Pytest** | Testing | ✅ Configured |
| **pytest-asyncio** | Async Test Support | ✅ Configured |

---

## 4. DEPENDENCIES ANALYSIS

### Python Dependencies (from pyproject.toml)

**Core Runtime:**
```
aiosqlite>=0.20.0          # Async SQLite
aiohttp>=3.10.10           # Async HTTP client
alembic>=1.13.2            # Database migrations
asyncpg>=0.30.0            # PostgreSQL driver
beautifulsoup4>=4.12.3     # HTML parsing
celery[redis]>=5.4.0       # Task queue
fastapi>=0.115.0           # Web framework
greenlet>=3.1.1            # Async support
httpx>=0.27.2              # HTTP client
pgvector>=0.3.5            # PostgreSQL vectors
psycopg[binary]>=3.2.3     # PostgreSQL driver
pydantic>=2.9.2            # Validation
pydantic-settings>=2.6.0   # Settings management
pypdf>=5.1.0               # PDF processing
python-json-logger>=2.0.7  # JSON logging
python-multipart>=0.0.12   # Form parsing
redis>=5.1.1               # Redis client
sqlalchemy>=2.0.36         # ORM
tenacity>=9.0.0            # Retry logic
uvicorn[standard]>=0.32.0  # ASGI server
```

**Development Dependencies:**
```
mypy>=1.13.0               # Type checking
pytest>=8.3.3              # Testing
pytest-asyncio>=0.24.0     # Async test support
ruff>=0.7.0                # Linting
```

### Frontend Dependencies (from package.json)

**Production:**
```
next@16.2.6                # Framework
react@19.2.0               # UI library
react-dom@19.2.0           # DOM binding
```

**Development:**
```
tailwindcss@^3.4.14        # Styling
typescript@^5.6.3          # Type safety
@types/react@^19.2.2       # React types
@types/node@^22.8.1        # Node types
postcss@^8.4.47            # CSS processor
autoprefixer@^10.4.20      # CSS vendor prefixes
```

---

## 5. LIBRARIES & PACKAGES INVENTORY

### Core Libraries
| Library | Module | Purpose |
|---------|--------|---------|
| FastAPI | nexlexhub.api | HTTP API framework |
| SQLAlchemy | nexlexhub.db | ORM and database abstraction |
| Pydantic | nexlexhub.core, nexlexhub.api | Data validation |
| Celery | nexlexhub.worker | Async task queue |
| pgvector | nexlexhub.db | Vector embeddings |
| BeautifulSoup4 | nexlexhub.scrapers | HTML parsing |
| PyPDF | nexlexhub.processing | PDF extraction |

### Processing Libraries
| Library | Module | Purpose |
|---------|--------|---------|
| Regex | nexlexhub.processing | Pattern matching |
| json | nexlexhub.* | JSON serialization |
| hashlib | nexlexhub.processing | Hash functions |

### Optional Libraries (Not in requirements)
```
sentence-transformers    # Embeddings (lazy-loaded, optional)
numpy                    # Numerical operations (optional)
pytorch                  # ML framework (not in requirements)
```

---

## 6. BUILD TOOLS & CONFIGURATION

### Python Build System
- **Build System:** setuptools + wheel
- **Package Format:** src-layout with `src/nexlexhub/`
- **Configuration:** `pyproject.toml` (PEP 517/518 compliant)
- **Entry Points:**
  - `nexlexhub-api` → `nexlexhub.api.main:run`
  - `nexlexhub-seed` → `nexlexhub.scripts.seed_demo:main`

### Docker Build
- **Base Image:** `python:3.11-slim`
- **Multi-layer:** No optimization (single stage)
- **Startup:** Runs alembic migrations, then uvicorn

### Docker Compose
- **Services:**
  - `postgres` (pgvector image, port 5432)
  - `redis` (Redis 7, port 6379)
  - `api` (FastAPI service, port 8000)
  - `worker` (Celery worker, no port)

### Frontend Build
- **Build Tool:** Next.js default (webpack-based)
- **TypeScript:** Configured with strict mode off
- **Linting:** TypeScript compiler (`tsc --noEmit`)

---

## 7. ENVIRONMENT VARIABLES

### Configuration Template (.env.example)

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `NEXLEXHUB_APP_NAME` | string | NexLexHub | Application name |
| `NEXLEXHUB_ENV` | string | dev | Environment (dev/prod) |
| `NEXLEXHUB_API_KEY` | string | dev-api-key | Master API key |
| `NEXLEXHUB_JWT_SECRET` | string | change-me | JWT signing secret |
| `NEXLEXHUB_JWT_ISSUER` | string | nexlexhub | JWT issuer claim |
| `NEXLEXHUB_DATABASE_URL` | string | postgresql+asyncpg://... | Async DB connection |
| `NEXLEXHUB_SYNC_DATABASE_URL` | string | postgresql+psycopg://... | Sync DB connection |
| `NEXLEXHUB_REDIS_URL` | string | redis://localhost:6379/0 | Redis connection |
| `NEXLEXHUB_ALLOWED_KEYS` | string | dev-api-key:admin | API key roles |
| `NEXLEXHUB_EMBEDDING_PROVIDER` | string | hash | Embedding provider |
| `NEXLEXHUB_EMBEDDING_DIMENSION` | int | 16 | Embedding dimension |
| `NEXLEXHUB_RATE_LIMIT_PER_MINUTE` | int | 120 | Rate limit threshold |
| `NEXLEXHUB_ENABLE_DEMO_SEED` | bool | true | Seed demo data on startup |
| `NEXLEXHUB_AUTO_INIT_DB` | bool | true | Auto-initialize DB schema |

**⚠️ CRITICAL ISSUES:**
- `JWT_SECRET` is hardcoded as "dev-jwt-secret" in config.py (line 14)
- Demo API key in default environment
- No production-ready secrets management

---

## 8. DATABASE TECHNOLOGIES

### PostgreSQL Schema

**Tables (13 total):**
1. `users` - User accounts and roles
2. `courts` - Court jurisdictions
3. `judges` - Judicial officers
4. `publishers` - News/case sources
5. `cases` - Legal cases
6. `statutes` - Legislative acts
7. `judgments` - Full judgment documents
8. `judgment_chunks` - Text chunks with embeddings
9. `citations` - Citation references
10. `precedents` - Case precedent links
11. `legal_events` - Legal news/events
12. `embeddings` - Vector embeddings (pgvector)
13. `alerts` - User alerts
14. `ai_conversations` - AI chat history

**Extensions:**
- `pgvector` - Vector similarity search

**Special Types:**
- `JSONB` - JSON storage with indexing
- `Vector(1024)` - 1024-dimensional embeddings

### Migration Strategy
- **Tool:** Alembic
- **Migration Files:** 3 versions
  - `20260509_0001_initial.py` - Base schema
  - `20260509_0002_platform_expansion.py` - Additional tables
  - `20260509_0003_embedding_1024.py` - Embedding dimension update

---

## 9. API ENDPOINTS INVENTORY

### Authentication
- `POST /auth/login` - User authentication → TokenResponse

### Search & Retrieval
- `POST /search` - Full-text search → list[CaseOut]
- `POST /semantic-search` - Semantic search → dict
- `GET /cases` - List all cases → list[CaseOut]
- `GET /citations` - List citations → list[dict]
- `GET /precedents` - List precedents → list[dict]
- `GET /statutes` - Search statutes → list[StatuteOut]
- `GET /timeline` - Legal timeline → list[dict]

### Analysis & Intelligence
- `POST /legal-analysis` - Deep legal analysis → LegalAnalysisResponse
- `POST /ai/chat` - Streaming AI chat → StreamingResponse
- `GET /ai/conversations` - Conversation history → list[ConversationOut]

### Management
- `GET /alerts` - User alerts → list[AlertOut]
- `GET /related-cases/{case_id}` - Related cases → list[dict]
- `GET /graph` - Citation graph snapshot → dict
- `GET /health` - Health check → dict

**Authentication Methods:**
- Bearer JWT token (`Authorization: Bearer <token>`)
- API Key (`X-API-Key: <key>`)

**RBAC Roles:**
- `reader` - Search/retrieval access
- `analyst` - AI analysis access
- `admin` - Full administrative access

---

## 10. THIRD-PARTY INTEGRATIONS

### None Currently Configured

**Optional/Planned:**
- OpenAI API (for AI features) - NOT configured
- Sentence Transformers (for embeddings) - Lazy-loaded, optional
- Ollama (local LLM) - Optional, not required

---

## 11. CONFIGURATION FILES

| File | Purpose | Status |
|------|---------|--------|
| `pyproject.toml` | Python project metadata | ✅ Complete |
| `.env.example` | Environment template | ✅ Complete |
| `alembic.ini` | DB migration config | ✅ Complete |
| `docker-compose.yml` | Container orchestration | ✅ Complete |
| `Dockerfile` | Container build | ✅ Complete |
| `frontend/tsconfig.json` | TypeScript config | ✅ Complete |
| `frontend/next.config.ts` | Next.js config | ✅ Minimal |
| `frontend/tailwind.config.ts` | Tailwind CSS config | ✅ Complete |

---

## 12. DOCUMENTATION FILES

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Main overview | ✅ Good |
| `architecture.md` | System design | ✅ Good |
| `deployment-guide.md` | Deployment instructions | ✅ Minimal |
| `developer-guide.md` | Development setup | ✅ Minimal |
| `setup-guide.md` | Installation guide | ✅ Minimal |
| `PROJECT_CODE_ATLAS.md` | Code structure | ✅ Present |
| `PROJECT_CODE_INDEX.md` | Code index | ✅ Minimal |
| `GRAPH.md` | Graph documentation | ✅ Detailed |
| `ML_planning.md` | ML system design | ✅ Detailed |
| `TODO.md` | General TODOs | ✅ Present |
| `TODO_fix.md` | Bug fixes | ✅ Complete (checked off) |
| `TODO_agent_pivot.md` | Agent work | ✅ Present |
| `TODO_structure_fix.md` | Structure work | ✅ Present |

---

## 13. DATA FILES

| File | Size | Purpose | Status |
|------|------|---------|--------|
| `articles.json` | 278 KB | Sample legal articles | ✅ Present |
| `final_blog_output.json` | 4.3 KB | Sample blog output | ✅ Present |
| `failed_logs.json` | 2 B | Empty log file | ⚠️ Empty |
| `supreme_court_articles.json` | 0 B | Empty articles file | ⚠️ Empty |
| `nexlexhub_processed.sql` | 542 B | SQL schema | ✅ Present |

### SQLite Databases
| Database | Size | Purpose |
|----------|------|---------|
| `legal_intelligence.db` | 16 KB | Development database |
| `livelaw_supremecourt.db` | 110 KB | Supreme Court data |
| `nexlexhub_processed.db` | 24 KB | Processed data |

---

## 14. ASSET INVENTORY

### Code Assets (src/nexlexhub/)
- ✅ API layer (complete)
- ✅ Database layer (complete)
- ✅ Security layer (complete)
- ✅ Processing pipeline (mostly complete)
- ✅ RAG system (mostly complete)
- ⚠️ Agent system (minimal stubs)
- ⚠️ Compliance system (minimal stubs)
- ⚠️ Graph builder (empty)
- ⚠️ Official sources (empty)
- ⚠️ Scrapers (empty)
- ⚠️ Scripts (incomplete)

### Frontend Assets (frontend/app/)
- ✅ Main pages structure
- ✅ Workspace shell
- ✅ Route structure
- ⚠️ Page implementations (mostly stubs)
- ⚠️ Components (minimal)

### Data Assets
- ✅ Sample articles (278 KB)
- ✅ SQLite databases (3 files)
- ⚠️ Supreme court articles (empty)

---

## 15. DEPLOYMENT ARTIFACTS

| File | Type | Status |
|------|------|--------|
| `Dockerfile` | Container | ✅ Present |
| `docker-compose.yml` | Orchestration | ✅ Present |
| `.github/` | CI/CD | ⚠️ Empty |
| `production/` | Deployment | ⚠️ Empty |
| `deployment-guide.md` | Documentation | ⚠️ Minimal |

**Missing:**
- GitHub Actions workflows
- Kubernetes manifests
- Health checks configuration
- Backup/restore scripts
- Monitoring/observability setup

---

## 16. KNOWN ISSUES FROM TODO FILES

### Completed Fixes
- ✅ FastAPI `/ask` endpoint fixed
- ✅ Scraper invalid arguments fixed
- ✅ Empty scraper files implemented
- ✅ Sleep timeout corrected
- ✅ HTML entity decoding fixed
- ✅ Import errors resolved
- ✅ Graphify tool refactored

### Pending Issues
None documented (all marked complete in TODO_fix.md)

---

## 17. SUMMARY STATISTICS

| Category | Count | Status |
|----------|-------|--------|
| **Python Modules** | 25+ | ✅ Active |
| **API Endpoints** | 14+ | ✅ Implemented |
| **Database Tables** | 14 | ✅ Implemented |
| **Database Migrations** | 3 | ✅ Complete |
| **Frontend Routes** | 9+ | ✅ Structured |
| **Configuration Files** | 8+ | ✅ Present |
| **Documentation Files** | 13+ | ⚠️ Variable Quality |
| **Dependencies (Python)** | 24+ | ✅ Current |
| **Dependencies (Frontend)** | 7+ | ✅ Current |
| **Total Lines of Code** | ~15,000+ | ⚠️ Unknown |

---

## NEXT STEPS

This inventory sets the foundation for architectural analysis. Key findings:

1. **Core systems are well-structured** - API, DB, security tiers exist
2. **Frontend routes exist but implementations are minimal** - Mostly page stubs
3. **Processing/RAG implemented** - Chunking, embedding, retrieval working
4. **Agent system is stub-based** - Needs actual LLM integration
5. **Compliance system is minimal** - Basic structure only
6. **No CI/CD configured** - GitHub Actions empty
7. **Documentation is good conceptually** - But missing operational details

---

*End of Phase 1 Inventory*
