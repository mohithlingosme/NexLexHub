# NexLexHub — Project Code Documentation (Pharse_1)

> This document was regenerated to match the **current code under `Pharse_1/`**.
> It focuses on what’s implemented and how the current entrypoints are wired.

## 1) What Phase 1 currently does (high-level)
Phase 1 has two main responsibilities:

1. **Scrape raw legal articles** from supported sources.
   - In this codebase, the “scraper entrypoint” files are now **thin wrappers** that call discovery engines in `nexlexhub.scrapers.discovery`.

2. **Extract structured legal intelligence** from a prepared “training corpus” JSON using **Ollama + Pydantic**, and store results in **SQLite** (`legal_blogs`).

## 2) Directory map (Pharse_1)
Key locations:
- `Pharse_1/Scraper/` — scraping entrypoints and (some) pipeline scripts
- `Pharse_1/Scraper/Data/` — data folders used by scrapers / pipelines
- `Pharse_1/Scraper/Data/Script/` — Ollama extraction pipeline (`Ai_pipelines.py`)
- `Pharse_1/README.md` — Phase 1 plan and conceptual workflow

## 3) Scraper entrypoints (thin wrappers)
The following files now just import a discovery engine, run it via `asyncio`, and print JSON.

### 3.1 `Pharse_1/Scraper/BarandBentch/Court_news/Sc.py`
**Purpose**: Supreme Court category scraping for **Bar & Bench**.

**Implementation**:
- Imports: `BarAndBenchSupremeCourtEngine` from `nexlexhub.scrapers.discovery`.
- `async def scrape() -> list[dict]`:
  - `records = await BarAndBenchSupremeCourtEngine().discover()`
  - returns `[record.__dict__ for record in records]`.
- CLI entrypoint:
  - `if __name__ == "__main__": print(json.dumps(asyncio.run(scrape()), indent=2))`

**Note**: The actual crawling/extraction/dedup logic lives inside the discovery engine, not in this wrapper.

---

### 3.2 `Pharse_1/Scraper/BarandBentch/Court_news/High_court's/AllahabadHC.py`
**Purpose**: Allahabad High Court scraping for **Bar & Bench**.

**Implementation**:
- Imports: `BarAndBenchAllahabadHighCourtEngine`.
- Same wrapper structure as `Sc.py`:
  - `discover()` → list of records
  - return `[record.__dict__ for record in records]`
  - print JSON to stdout when executed directly

---

### 3.3 `Pharse_1/Scraper/Live_Law/SC.py`
**Purpose**: Supreme Court scraping for **LiveLaw**.

**Implementation**:
- Imports: `LiveLawSupremeCourtEngine`.
- Same wrapper structure as above:
  - `await engine.discover()`
  - transform each record using `record.__dict__`
  - print JSON when run directly

## 4) Ollama extraction pipeline (SQLite writer)
### 4.1 `Pharse_1/Scraper/Data/Script/Ai_pipelines.py`
**Purpose**: Turn a pre-built training corpus JSON into structured legal intelligence via Ollama, validate with Pydantic, and persist to SQLite.

#### 4.1.1 Runtime configuration
Hard-coded in this file:
- `INPUT_JSON`: absolute path to `Final_training_corpus.json`
- `DATABASE_FILE = "legal_intelligence.db"`
- `OLLAMA_MODEL = "llama3"`
- `LOG_FILE = "pipeline.log"`

#### 4.1.2 Logging
- Uses `logging.basicConfig` with both:
  - `logging.FileHandler(LOG_FILE, encoding="utf-8")`
  - `logging.StreamHandler()`

#### 4.1.3 Data model (Pydantic)
`LegalIntelligence(BaseModel)` includes defaults for:
- `title`, `introduction`, `facts`, `procedural_history`
- `issues`, `principles`, `statutes`, `precedents` (all `List[str]`)
- `findings`, `final_ruling`, `significance`
- `confidence_score: float`

#### 4.1.4 SQLite schema creation
`init_db(db_file)`:
- `CREATE TABLE IF NOT EXISTS legal_blogs` with:
  - dedupe key: `source_hash TEXT UNIQUE`
  - provenance: `source_file TEXT`
  - structured fields + list fields stored as JSON strings
  - `created_at TEXT`

#### 4.1.5 Safe JSON extraction
`extract_json(text)`:
- tries `json.loads(text)` directly
- if that fails, attempts to slice between the first `{` and the last `}` and parses that
- returns `None` on failure

#### 4.1.6 Ollama analysis prompt
`analyze_case(case_text)`:
- Builds a strict prompt instructing Ollama to output **ONLY JSON** and to include all fields.
- Calls:
  - `ollama.chat(model=OLLAMA_MODEL, messages=[{"role":"user","content": prompt}])`
- Extracts `response["message"]["content"]`
- Parses+validates:
  - `parsed = extract_json(content)`
  - `validated = LegalIntelligence(**parsed)`

#### 4.1.7 Dedupe key
`generate_hash(text)`:
- SHA-256 over the `case_text` (used as `source_hash`).

#### 4.1.8 Insert behavior
`insert_to_legal_blogs(conn, intel, source_hash, source_file)`:
- Uses `INSERT OR IGNORE INTO legal_blogs (source_hash UNIQUE ...)`
- Escapes fields using `html.escape` for text fields.
- Serializes list fields using `json.dumps(..., ensure_ascii=False)`.
- Sets:
  - `slug = slugify(intel.title or "untitled")`
  - `created_at = datetime.now().isoformat()`

#### 4.1.9 Corpus loading & main loop
- `load_corpus(file_path)` loads JSON and returns the list (or `[]` on error).
- `get_case_text(entry)` tries keys in order when `entry` is dict:
  - `text`, `content`, `judgment`, `document`, `case_text`
  - otherwise stringifies `entry`.
- `main()`:
  - initializes DB
  - loads corpus
  - iterates entries with `tqdm`
  - for each entry:
    - compute `source_hash`
    - `intel = analyze_case(case_text)`
    - insert into SQLite
  - logs success/failed counts

#### 4.1.10 Entry point
Runs `main()` when invoked directly.

## 5) How to use the regenerated entrypoints
- To run scraping wrappers:
  - Run `Sc.py` / `Live_Law/SC.py` / AllahabadHC wrapper
  - They print discovered records as JSON to stdout.

- To run the Ollama extraction:
  - Run `Pharse_1/Scraper/Data/Script/Ai_pipelines.py`
  - It reads `INPUT_JSON` (currently hard-coded) and writes to `legal_intelligence.db`.

## 6) Known limitations
- Scraper behavior (URL discovery, scraping, parsing, dedupe) is currently implemented inside `nexlexhub.scrapers.discovery` discovery engines. This document can only describe what’s visible in the Phase 1 wrapper files plus the SQLite/Ollama pipeline.
- `INPUT_JSON` is hard-coded as an absolute Windows path; updating it may be required when moving machines.


