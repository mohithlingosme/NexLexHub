# AI Legal News Agent

Production-grade pipeline for scraping, cleaning, chunking, and AI-processing legal news from LiveLaw.in.

## 🚀 Quick Start

```bash
# Install deps
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Run full pipeline
cd ai-legal-news-agent
python main.py all

# Or step by step
python main.py scrape
python main.py clean
python main.py chunk
python main.py summarize
```

## 📁 Structure

- `data/raw/` → Raw scraped articles
- `data/processed/` → Cleaned articles
- `data/chunks/` → Chunked data for RAG
- `scraper/` → LiveLaw scraper
- `pipeline/` → ETL pipeline
- `ai/` → LLM processing + embeddings/RAG
- `utils/` → Helpers

## Pipeline Flow

```
scrape → clean → dedup → chunk → summarize → embed → RAG
```

## Config

- Ollama URL: `http://localhost:11434` (llama3 model)
- Update `utils/config.py` for custom settings

