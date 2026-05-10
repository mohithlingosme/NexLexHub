# PROJECT_CODE_INDEX.md

Quick index for `PROJECT_CODE_ATLAS.md`.

## Phase 1 Legacy (in this environment)
### Scraper entrypoints
- `Pharse_1/Scraper/BarandBentch/Court_news/Sc.py`
  - Async discovery via `BarAndBenchSupremeCourtEngine`.
- `Pharse_1/Scraper/Live_Law/SC.py`
  - Async discovery via `LiveLawSupremeCourtEngine`.

### Pipeline / AI extraction
- `Pharse_1/Scraper/Data/Script/Ai_pipelines.py`
  - Loads JSON corpus → Ollama extraction → Pydantic validate → SQLite insert.

### Legacy DB schema
- `Pharse_1/database/nexlexhub_schema.sql`
  - Tables: legal_documents, processing_logs, failed_ingestions, source_registry.

## Files not reliably accessible for “every line” in this environment
- Any `core/legal_pipeline/*` at repo root (read attempts failed due to missing paths).
- Any `apps/api/main.py` at repo root (read attempts failed due to missing paths).

If these exist elsewhere in your repo, I can regenerate the atlas once we identify the correct physical paths.
