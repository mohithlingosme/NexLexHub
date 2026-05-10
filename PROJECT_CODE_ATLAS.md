# PROJECT_CODE_ATLAS.md (Phase 1 Legacy Scope)

This document is intended to be *attached* to AI responses to explain how **NexLexHub Phase 1 legacy** is structured and how code flows.

> Note: Full “each and every line” coverage requires reading every file in-scope. In this environment, several paths you referenced (e.g. `core/legal_pipeline/*` at repo root) did not exist; the reliable in-repo Phase 1 scope is under `Pharse_1/`.

## 1) What Phase 1 Legacy is (high-level)
Phase 1 legacy provides:
- Scrapers for Supreme Court / Bar & Bench / LiveLaw, plus some per-HC scripts.
- Data cleaning / filtering / chunking scripts.
- An ML/LLM-style “pipeline” script that extracts structured legal intelligence from article/judgment text using **Ollama**.
- Output persistence into a local SQLite database.

Key folders:
- `Pharse_1/Scraper/` : web scraping & ingestion into JSON/DB.
- `Pharse_1/Processing/` : dedup/corpus processing.
- `Pharse_1/Core_pipeline.py` : older end-to-end pipeline scaffold.
- `Pharse_1/Scraper/Data/Script/` : chunking/cleaning/pipeline helper scripts.

## 2) Entry points (where execution starts)
### 2.1 `Pharse_1/Scraper/BarandBentch/Court_news/Sc.py`
- Imports `nexlexhub.scrapers.discovery.BarAndBenchSupremeCourtEngine`.
- Runs async `discover()`.
- Prints discovered records as JSON.

Code excerpt (order of appearance):
1. Imports: `asyncio`, `json`.
2. Imports discovery engine from `nexlexhub.scrapers.discovery`.
3. Defines `async def scrape() -> list[dict]`:
   - `records = await ...Engine().discover()`
   - Returns `[record.__dict__ for record in records]`.
4. `if __name__ == "__main__":`:
   - `print(json.dumps(asyncio.run(scrape()), indent=2))`

### 2.2 `Pharse_1/Scraper/Live_Law/SC.py`
Same structure as `Sc.py`, but uses:
- `nexlexhub.scrapers.discovery.LiveLawSupremeCourtEngine`.

### 2.3 `Pharse_1/Scraper/Data/Script/Ai_pipelines.py`
This is a more monolithic “pipeline” script that:
- Loads a JSON corpus.
- For each entry, extracts case text.
- Calls Ollama (`llama3`) to produce a structured `LegalIntelligence` object as JSON.
- Validates with Pydantic.
- Inserts results into SQLite table `legal_blogs` (dedup by SHA256 of case text).

#### 2.3.1 Imports (functional grouping)
- Standard libs: `os`, `json`, `sqlite3`, `logging`, `hashlib`, `html`, `Path`, `datetime`, typing.
- External libs:
  - `ollama` : LLM calls
  - `pydantic` : schema validation
  - `slugify` : slug generation
  - `tqdm` : progress bar

#### 2.3.2 Configuration constants
- `INPUT_JSON` : points to `Pharse_1/Scraper/Data/Filter/Supreme_Court/Final_training_corpus.json`
- `DATABASE_FILE = "legal_intelligence.db"`
- `OLLAMA_MODEL = "llama3"`
- `LOG_FILE = "pipeline.log"`

#### 2.3.3 Logging setup
- `logging.basicConfig(...)` writes to `pipeline.log` and stdout.

#### 2.3.4 Pydantic model: `LegalIntelligence`
Defines fields expected from Ollama:
- `title`, `introduction`, `facts`, `procedural_history`
- list fields: `issues`, `principles`, `statutes`, `precedents`
- `findings`, `final_ruling`, `significance`
- `confidence_score: float` (default 0.0)

#### 2.3.5 DB initialization: `init_db(db_file)`
- Ensures parent dir exists.
- Creates `legal_blogs` table with columns matching the model fields.
- Commits and returns SQLite connection.

#### 2.3.6 Hashing: `generate_hash(text)`
- Uses SHA256 of the case text.

#### 2.3.7 Safe JSON extraction: `extract_json(text)`
- First attempts `json.loads(text)`.
- If fails, tries to find outer `{ ... }` block.
- Returns parsed JSON or `None`.

#### 2.3.8 Ollama analysis: `analyze_case(case_text)`
- Builds a prompt that instructs model to output **ONLY VALID JSON**.
- Calls:
  - `ollama.chat(model=OLLAMA_MODEL, messages=[{role:"user", content: prompt}])`
- Reads response at `response["message"]["content"]`.
- Parses JSON with `extract_json`.
- Validates with `LegalIntelligence(**parsed)`.
- Returns validated model or `None` on any failure.

#### 2.3.9 Insert into DB: `insert_to_legal_blogs(...)`
- Executes an `INSERT OR IGNORE INTO legal_blogs (...)` statement.
- `source_hash` is `UNIQUE` so duplicates skip.
- Escapes fields using `html.escape(...)` and serializes lists with `json.dumps(...)`.
- Commits.
- Logs whether an insert happened via `conn.total_changes`.

#### 2.3.10 Load corpus: `load_corpus(file_path)`
- Reads JSON array from `INPUT_JSON`.

#### 2.3.11 Extract case text: `get_case_text(entry)`
- If `entry` is dict:
  - checks keys in `["text","content","judgment","document","case_text"]`.
- Otherwise returns `str(entry)`.

#### 2.3.12 Main loop: `main()`
- Initializes DB.
- Loads corpus.
- Iterates entries with `tqdm`:
  1. `case_text = get_case_text(entry)`
  2. skip empty/whitespace case text
  3. compute `source_hash`
  4. `intel = analyze_case(case_text)`
  5. if intel exists insert into DB
  6. count successes/failures
- Closes connection.

#### 2.3.13 Script entry
- `if __name__ == "__main__": main()`

## 3) Database schema (Phase 1 legacy)
### 3.1 `Pharse_1/database/nexlexhub_schema.sql`
Defines:
- `legal_documents` (primary legal intelligence table)
- `automotive_documents` (unrelated placeholder)
- `processing_logs`
- `failed_ingestions`
- `source_registry`
- Alembic/MySQL-like timestamp update triggers

## 4) Gaps / path mismatches detected in this environment
- Several “Phase 1 legacy” files you opened are shown in your tabs as:
  - `core/legal_pipeline/*.py`
  - `apps/api/main.py`
- But reading those paths from the repo root failed, indicating those files may exist under a different root (e.g. inside `src/` or not present at all).

This atlas therefore currently covers only the Phase 1 files that were successfully read from disk.

## 5) Suggested next step to satisfy “every line”
To truly comply with “each and every line of code”, run a repository-wide Phase 1 export where we:
1. Enumerate all `.py` files under `Pharse_1/`.
2. Generate a concatenated per-file listing with exact line numbers.
3. Produce a markdown appendix that describes blocks in order.

Because the environment tool currently has path resolution failures for root-level `core/legal_pipeline`, Phase 1 legacy scope should be anchored strictly to the `Pharse_1/` directory.

