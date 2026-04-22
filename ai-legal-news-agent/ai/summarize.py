import json
import requests
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.file_utils import load_json, save_json, is_valid, get_hash

logger = logging.getLogger(__name__)

INPUT_FILE = "data/processed/clean_articles.json"
OUTPUT_FILE = "data/processed/processed_articles.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

MAX_WORKERS = 3
SAVE_EVERY = 20

def build_prompt(article):
    return f\"\"\"Return ONLY valid JSON object.

{{
  "headline": "short engaging headline",
  "intro": "100-word summary",
  "analysis": "200-word legal analysis",
  "legal_principles": ["principle 1", "principle 2"],
  "conclusion": "key takeaway"
}}

Article Title: {article.get("title","")}
Content (first 2000 chars): {article.get("content","")[:2000]}
\"\"\"

def call_ollama(prompt):
    try:
        res = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=120
        )
        return res.json().get("response", "")
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        return ""

def extract_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end <= start:
            return None
        return json.loads(text[start:end])
    except:
        return None

def process_article(article):
    prompt = build_prompt(article)
    raw_response = call_ollama(prompt)
    parsed = extract_json(raw_response)
    
    if not parsed:
        # Fallback
        parsed = {
            "headline": article.get("title", ""),
            "intro": article.get("content", "")[:200],
            "analysis": "",
            "legal_principles": [],
            "conclusion": ""
        }
    
    return {
        "title": article.get("title"),
        "date": article.get("date"),
        "url": article.get("url"),
        "ai_summary": parsed
    }

def main():
    logger.info("Starting AI summarization...")
    articles = load_json(INPUT_FILE)
    articles = [a for a in articles if is_valid(a)]
    
    # Dedup
    seen = set()
    unique_articles = []
    for a in articles:
        h = get_hash(a)
        if h not in seen:
            seen.add(h)
            unique_articles.append(a)
    
    logger.info(f"Processing {len(unique_articles)} unique articles")
    
    processed = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_article, a) for a in unique_articles]
        
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            processed.append(result)
            
            logger.info(f"Processed {i+1}/{len(unique_articles)}")
            
            if (i + 1) % SAVE_EVERY == 0:
                save_json(processed, OUTPUT_FILE)
    
    save_json(processed, OUTPUT_FILE)
    logger.info("AI summarization complete!")

if __name__ == "__main__":
    main()

