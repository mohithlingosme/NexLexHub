# Implementation Plan

## Overview
Create a production-ready Python module in the `core/legal_pipeline/` directory for processing Supreme Court case data from `Pharse_1/Scraper/Data/Filter/Supreme_Court/Final_training_corpus.json`. The module will use Ollama for structured reasoning, Serper API for web search augmentation, and generate both HTML blog formats and SQL INSERT statements for the `supreme_court_cases` table. This fits into the existing `core/` structure alongside `ai/llm_client.py`, `pipeline/processor.py`, and `schema/legal_document.py`, extending the legal AI pipeline for batch processing of structured legal content.

The input JSON contains pre-processed Supreme Court articles with fields like `title`, `content`, `url`, `court`, `date`, etc. Each entry will be transformed into the strict 8-section format using LLM reasoning enhanced by web search on case title + key terms. Output per case: HTML file and SQL INSERT. Support batch processing, error handling, logging, and web search fallback (direct LLM without search).

## Types
Pydantic models for structured data flow:

1. **SupremeCourtCase** (input schema matching JSON):
   - id: str
   - title: str
   - content: str  
   - url: str
   - date: str
   - source: str
   - category_tags: List[str]

2. **LegalBlogStructure** (strict 8-section output):
   - background: str
   - procedural_history: str
   - findings: str
   - principles: List[str]  # Bullet points
   - statutory_framework: str
   - precedents: List[str]  # Bullet points
   - final_ruling: str
   - conclusion: str

3. **PipelineOutput**:
   - case: SupremeCourtCase
   - structured: LegalBlogStructure
   - html_content: str
   - sql_insert: str
   - search_results: Optional[List[str]]  # Serper snippets
   - processed_at: datetime

Validation ensures no sections skipped, formal tone, insights from content + search.

## Files
Create new modular files under `core/legal_pipeline/` (auto-creates dir):

- **New files**:
  | Path | Purpose |
  |------|---------|
  | `core/legal_pipeline/__init__.py` | Package init, re-export main classes |
  | `core/legal_pipeline/web_search.py` | Serper API client with queries like f\"{title} Supreme Court case analysis precedents\" |
  | `core/legal_pipeline/ollama_client.py` | Specialized LLM prompts for 8-section structuring + search augmentation |
  | `core/legal_pipeline/processor.py` | Main orchestrator: load JSON → batch process → generate HTML/SQL → save |
  | `core/legal_pipeline/output_generators.py` | HTML templating (semantic <h1>-<ul>) + SQL INSERT escaping |
  | `core/legal_pipeline/types.py` | Pydantic models above |
  | `core/legal_pipeline/runner.py` | CLI entrypoint: `python -m core.legal_pipeline.runner` |

- **Modified files**:
  | Path | Changes |
  |------|---------|
  | `core/config.py` | Add `SERPER_API_KEY: str = os.getenv("SERPER_API_KEY")`<br>Add `LEGAL_PIPELINE_OUTPUT_DIR: str = "data/legal_pipeline/output"` |
  | `requirements.txt` | Append `serper` (Serper client) |
  | `core/schema/legal_document.py` | Optional: Extend with SupremeCourtCase for consistency |

- **No deletions/moves**.

Output directories: `data/legal_pipeline/html/`, `data/legal_pipeline/sql/`, `data/legal_pipeline/json/` (raw outputs).

## Functions
New functions with signatures/purpose:

- **web_search.py**:
  - `search_case_context(title: str, content_snippet: str) -> List[str]`: Top 3-5 Serper results → snippets.

- **ollama_client.py**:
  - `structure_case(case: SupremeCourtCase, search_snippets: List[str]) -> LegalBlogStructure`: Strict prompt enforcing sections.

- **output_generators.py**:
  - `generate_html(structured: LegalBlogStructure, title: str) -> str`: Semantic HTML.
  - `generate_sql(case: SupremeCourtCase, structured: LegalBlogStructure) -> str`: Escaped INSERT for `supreme_court_cases`.

- **processor.py**:
  - `async process_single(case: SupremeCourtCase) -> PipelineOutput`
  - `async process_batch(json_path: Path, batch_size: int = 5) -> List[PipelineOutput]`

- **runner.py**:
  - `main()`: Load input JSON → batch process → save outputs.

All functions: async where API-bound, logging, retries, fallback (search fail → LLM only).

## Classes
No major class changes; functional modular approach. Minor:

- **LegalPipelineProcessor** (processor.py): Stateful batch processor with logging.

## Dependencies
- **New**: `serper` (`pip install serper`)
- **Existing**: Extend `httpx`, `ollama` (via llm_client.py), `pydantic`.
- Env: `SERPER_API_KEY` required (user must provide).

Update `requirements.txt` atomically.

## Testing
- **New test file**: `core/legal_pipeline/test_processor.py`
  - `test_structure_prompts()`: Mock LLM, validate sections non-empty.
  - `test_html_sql_output()`: Render → parse HTML/SQL validity.
  - `test_batch_errors()`: Resilience (empty content, API fail).
- Run: `pytest core/legal_pipeline/`
- Integration: Process 1-2 sample cases from input JSON.

Manual: `python -m core.legal_pipeline.runner --input <json_path> --limit 3`

## Implementation Order
1. Create `core/legal_pipeline/types.py` (schemas).
2. Create `core/legal_pipeline/web_search.py` + update `core/config.py`.
3. Create `core/legal_pipeline/ollama_client.py` (prompts).
4. Create `core/legal_pipeline/output_generators.py`.
5. Create `core/legal_pipeline/processor.py`.
6. Create `core/legal_pipeline/runner.py` + `__init__.py`.
7. Update `requirements.txt`.
8. Add tests `core/legal_pipeline/test_processor.py`.
9. Test run: `python -m core.legal_pipeline.runner` on sample JSON.
10. Document usage in `README.md` under core/legal_pipeline.


