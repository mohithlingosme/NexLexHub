# NexLexHub Pharse_1 Production Pipeline

## 🚀 Quick Start

1. **Install deps:**
```
pip install -r Pharse_1/Scraper/Script/requirements.txt
```

2. **Ollama model:**
```
ollama pull qwen2.5  # or llama3.1
```

3. **Config (.env):**
```
cp Pharse_1/Scraper/Script/.env.example .env
edit .env  # MySQL creds optional
```

4. **Run pipeline:**
```
cd Pharse_1/Scraper/Script
python Ai_pipelines.py
```

## 📁 Structure
```
Pharse_1/Scraper/Data/
├── Raw/           # Drop .txt .md .json .html here
├── Processed/     # Auto-populated
├── Output/        # SQL dumps
└── database/      # SQLite + schema
```

## 🧪 Test
```
pytest  # Later tests/
```

## 🔧 Deployment
- MySQL: `mysql < Output/nexlexhub_mysql_dump.sql`
- Resume-safe: Checks source_registry
- Logs: processing_logs table
- Metrics: avg confidence, failures

## Future
- LegalOS KG
- Autopredator automotive
- Ollama fine-tune
