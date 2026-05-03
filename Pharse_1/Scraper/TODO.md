# NexLexHub Pharse_1 Productionization TODO

Approved Plan Steps (User-confirmed with schema/DB/logging expansions):

**Progress Tracking:**
task_progress Items:
- [x] Step 1: config.py + .env ✅
- [x] Step 2: database schema + SQLite init ✅
- [x] Step 3: cleaner.py ✅
- [ ] Step 4: chunker.py
- [ ] Step 5: validator.py
- [x] Step 6: sql_exporter.py ✅
- [x] Step 7: Ai_pipelines.py ✅
- [x] Step 8: tests/ ✅
- [ ] Step 9: Restructure folders
- [ ] Step 10: CLI + README
- [ ] Step 11: Dry-run + validate
- [ ] Step 12: Complete ✅

**Post-Edit Steps:**
- pip install -r requirements.txt (pydantic, ollama, PyMySQL, etc.)
- cp .env.example .env; edit MySQL creds
- python -m Pharse_1.Scraper.Script.Ai_pipelines --input-dir Data/Raw --model qwen2.5
- pytest tests/
- mysql -u root nexlexhub < nexlexhub_mysql_dump.sql

