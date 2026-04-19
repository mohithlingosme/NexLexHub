import json
import requests
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_FILE = "clean_articles.json"
OUTPUT_FILE = "processed_articles.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

MAX_WORKERS = 3   # ⚠️ increase slowly (3–5 max)
SAVE_EVERY = 20


# =========================
# 📥 LOAD
# =========================

def load_articles():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    try:
        return json.loads(content)
    except:
        return [json.loads(line) for line in content.split("\n") if line]


# =========================
# 🧹 BASIC FILTER
# =========================

def is_valid(article):
    content = article.get("content", "")
    return bool(content and len(content) > 150)


# =========================
# 🔁 DEDUPLICATION
# =========================

def get_hash(article):
    text = article.get("title", "") + article.get("content", "")[:200]
    return hashlib.md5(text.encode()).hexdigest()


# =========================
# 🧠 PROMPT
# =========================

def build_prompt(article):
    return f"""
Return ONLY JSON.

{{
 "headline": "",
 "intro": "",
 "analysis": "",
 "legal_principles": [],
 "conclusion": ""
}}

Title: {article.get("title","")}
Content: {article.get("content","")[:500]}
"""


# =========================
# 🤖 OLLAMA CALL
# =========================

def call_ollama(prompt):
    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        return res.json().get("response", "")
    except:
        return ""


# =========================
# 🧹 JSON EXTRACT
# =========================

def extract_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except:
        return None


# =========================
# 🛟 FALLBACK
# =========================

def fallback(article):
    return {
        "headline": article.get("title", ""),
        "intro": article.get("content", "")[:200],
        "analysis": "",
        "legal_principles": [],
        "conclusion": ""
    }


# =========================
# ⚙️ PROCESS ONE
# =========================

def process_article(article):
    prompt = build_prompt(article)
    raw = call_ollama(prompt)

    data = extract_json(raw)

    if not data:
        data = fallback(article)

    return {
        "title": article.get("title"),
        "date": article.get("date"),
        "url": article.get("url"),
        "content": data
    }


# =========================
# 🚀 MAIN
# =========================

def main():
    articles = load_articles()
    articles = [a for a in articles if is_valid(a)]

    print(f"📥 TOTAL: {len(articles)}")

    # deduplicate
    seen = set()
    unique_articles = []

    for a in articles:
        h = get_hash(a)
        if h not in seen:
            seen.add(h)
            unique_articles.append(a)

    print(f"✅ UNIQUE: {len(unique_articles)}")

    output = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_article, a) for a in unique_articles]

        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            output.append(result)

            print(f"✅ processed {i+1}")

            if (i + 1) % SAVE_EVERY == 0:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(output, f, indent=2)
                print(f"💾 saved {len(output)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("🎉 DONE")


if __name__ == "__main__":
    main()