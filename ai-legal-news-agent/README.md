# AI Legal News Agent

Production-grade pipeline for scraping, cleaning, deduplicating, chunking, and AI-summarizing legal news from LiveLaw.in.

## Setup

```bash
cd ai-legal-news-agent
pip install -r requirements.txt
playwright install
```

If you want AI summaries and embeddings:

```bash
# Start Ollama separately, then pull the models you want:
ollama pull llama3
ollama pull nomic-embed-text
```

## Run

```bash
# End-to-end
python main.py full

# End-to-end + embeddings (builds `data/processed/vector_store.json`)
python main.py full --with-embeddings

# Step-by-step
python main.py scrape --max-pages 10
python main.py clean
python main.py dedup
python main.py chunk
python main.py summarize
python main.py embed
```

## Output

- `data/raw/articles.json` — raw scraped articles
- `data/processed/clean_articles.json` — cleaned articles
- `data/processed/deduplicated_articles.json` — deduplicated articles
- `data/chunks/chunk_*.json` — chunks for retrieval
- `data/processed/processed_articles.json` — AI summaries
- `data/processed/vector_store.json` — lightweight vector store for retrieval

## Embeddings + RAG (optional)

```bash
# Build a lightweight vector store from chunk files
python -m ai.embed

# Retrieve + answer (uses Ollama if available)
python -m ai.rag
```

## Notes

- Scraping uses Playwright; you must run `playwright install` once.
- Summarization uses Ollama when available; otherwise a deterministic fallback summary is used so the pipeline still runs.
