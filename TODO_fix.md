# NexLexHub Fix TODO

- [x] 1. Fix `Assets/ai-legal-news-agent/server.py` — `/ask` endpoint missing `retrieve()` call
- [x] 2. Fix `Assets/ai-legal-news-agent/scraper/indiakanoon_scraper.py` — invalid `text_content("")` argument
- [x] 3. Implement `Pharse_1/Scraper/Live_Law/High Court/Karnataka_HC.py` — file is empty
- [x] 4. Fix `Assets/ai-legal-news-agent/pipeline/processor.py` — post-scrape sleep should be `wait_for` timeout
- [x] 5. Rename `Pharse_1/Neural_Scheme.html` → `Pharse_1/Neural_Scheme.py`
- [x] 6. Fix `Pharse_1/Scraper/Bar&Bentch_Scraper.py` — decode HTML entities
- [x] 7. Fix `Assets/ai-legal-news-agent/config.py` — add missing `Dict` import
- [x] 8. Fix `tools/graphify.py` — Mermaid ID collisions + missing `.pytest_cache` exclusion
- [x] 9. Refactor `tools/graphify.py` — typed dicts, logging, exclusions, tests (25 passed)

