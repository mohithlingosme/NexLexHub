import re
import json
import hashlib

INPUT_FILE = "articles.json"


# =========================
# 📥 LOAD + RECOVER
# =========================

def load_articles():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    matches = re.findall(r'\{.*?"date":.*?\}', text, re.DOTALL)

    data = []

    for i, m in enumerate(matches):
        try:
            obj = json.loads(m)
            data.append(obj)
        except:
            continue

    print(f"✅ Extracted {len(data)} raw objects")
    return data


# =========================
# 🧹 CLEAN FILTER
# =========================

def is_valid(article):
    title = article.get("title")
    content = article.get("content")
    date = article.get("date")

    # must have all 3
    if not title or not content or not date:
        return False

    # remove MCQ / exam junk
    if "question" in content.lower() or "mcq" in content.lower():
        return False

    # remove very small content
    if len(content) < 200:
        return False

    return True


# =========================
# 🔁 DEDUP
# =========================

def get_hash(article):
    text = article["title"] + article["content"][:200]
    return hashlib.md5(text.encode()).hexdigest()


# =========================
# 🚀 MAIN CLEANER
# =========================

def main():
    raw = load_articles()

    cleaned = []
    seen = set()

    for article in raw:
        if not is_valid(article):
            continue

        h = get_hash(article)

        if h in seen:
            continue

        seen.add(h)

        cleaned.append({
            "title": article["title"].strip(),
            "content": article["content"].strip(),
            "date": article["date"]
        })

    print(f"✅ FINAL CLEAN ARTICLES: {len(cleaned)}")

    with open("clean_articles.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)

    print("💾 Saved clean_articles.json")


if __name__ == "__main__":
    main()