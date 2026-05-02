import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timezone

INPUT_PATH = Path(r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Raw_Data\SC_articles.json")
OUTPUT_PATH = Path(r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Cleaned data\Cleaned_Sc_articles.json")

CHUNK_SIZE = 1800


def generate_id(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_whitespace(text):
    return re.sub(r"\s+", " ", str(text)).strip()


def clean_text(text):
    if not text:
        return ""

    patterns = [
        r"\[ARTICLE\]",
        r"\[CONTENT\]",
        r"\[Read Order\]",
        r"\[Read Live Coverage\]",
        r"\[Live Coverage\]",
        r"Source:\s*[A-Za-z& ]+",
        r"Date:\s*\d{4}-\d{2}-\d{2}T[\d:+-Z]+",
        r"Title:\s*",
    ]

    for p in patterns:
        text = re.sub(p, " ", text, flags=re.IGNORECASE)

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\xa0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"T\d{2}:\d{2}:\d{2}Z", "", text)
    text = re.sub(r"\.\.+", ".", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1. \2", text)
    text = re.sub(r"\s+\.", ".", text)
    text = re.sub(r"\s+,", ",", text)

    return normalize_whitespace(text)


def detect_court(content, title):
    combined = f"{title} {content}".lower()

    if "supreme court" in combined:
        return "Supreme Court"
    elif "high court" in combined:
        return "High Court"
    elif "tribunal" in combined:
        return "Tribunal"

    return "Unknown"


def extract_case_references(content):
    refs = set()

    matches = re.findall(
        r"([A-Z][A-Za-z .,&]+?\sv\.\s[A-Z][A-Za-z .,&]+)",
        content
    )

    for match in matches:
        cleaned = normalize_whitespace(match).strip(" .,")

        if 15 < len(cleaned) < 250:
            refs.add(cleaned)

    return sorted(refs)


def extract_judges(content):
    judges = set()

    singular = re.findall(
        r"Justice\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        content
    )

    for name in singular:
        full = f"Justice {name.strip()}"
        if len(full.split()) >= 3:
            judges.add(full)

    plural = re.findall(
        r"Justices\s+([A-Z][A-Za-z\s,&]+)",
        content
    )

    for block in plural:
        names = re.split(r",|and", block)

        for name in names:
            name = name.strip()
            if len(name.split()) >= 2:
                judges.add(f"Justice {name}")

    invalid = [
        "said", "remarked", "court",
        "bench", "approval", "application"
    ]

    final = []

    for judge in judges:
        if not any(bad in judge.lower() for bad in invalid):
            final.append(judge)

    return sorted(set(final))


def extract_legal_entities(content):
    entities = set()

    patterns = [
        r"Article\s+\d+[A-Z]?",
        r"BNSS",
        r"IPC",
        r"CrPC",
        r"Constitution",
        r"Bharatiya Nagarik Suraksha Sanhita",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content, flags=re.IGNORECASE)
        for m in matches:
            entities.add(m.strip())

    return sorted(entities)


def classify_categories(content):
    c = content.lower()
    categories = set()

    mapping = {
        "criminal": ["bail", "crime", "criminal", "arrest"],
        "corporate": ["company", "shareholder", "investor"],
        "constitutional": ["constitution", "article", "fundamental rights"],
        "civil": ["property", "injunction"],
        "insolvency": ["insolvency", "bankruptcy"],
        "regulatory": ["compliance", "authority"],
    }

    for cat, keywords in mapping.items():
        if any(word in c for word in keywords):
            categories.add(cat)

    if not categories:
        categories.add("general_legal")

    return sorted(categories)


def chunk_text(text):
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)

        if len(" ".join(current)) >= CHUNK_SIZE:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


def process_article(article):
    title = normalize_whitespace(article.get("title", ""))
    raw_content = article.get("content", "")

    cleaned = clean_text(raw_content)

    if not cleaned:
        return None

    judges = extract_judges(cleaned)
    chunks = chunk_text(cleaned)

    return {
        "id": generate_id(article.get("url", "") + title),
        "url": article.get("url", ""),
        "title": title,
        "author": article.get("author") or "Unknown",
        "source": article.get("source", ""),
        "court": detect_court(cleaned, title),
        "date": article.get("date", ""),
        "content": cleaned,
        "summary_ready_content": cleaned[:5000],
        "category_tags": classify_categories(cleaned),
        "legal_entities": extract_legal_entities(cleaned),
        "case_references": extract_case_references(cleaned),
        "judges": judges,
        "bench_strength": str(len(judges)) if judges else "Unknown",
        "content_type": "legal_news",
        "chunks": chunks,
        "chunk_count": len(chunks),
        "word_count": len(cleaned.split()),
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "pipeline_version": "phase_12_debugged_final",
        "qa_score": 10
    }


def main():
    print("=" * 60)
    print("NexLexHub SC Cleaner Phase 12 Debugged Final")
    print("=" * 60)

    if not INPUT_PATH.exists():
        print(f"INPUT FILE NOT FOUND:\n{INPUT_PATH}")
        return

    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            raw_articles = json.load(f)

    except Exception as e:
        print(f"FAILED TO LOAD JSON: {e}")
        return

    print(f"TOTAL RAW ARTICLES FOUND: {len(raw_articles)}")

    processed_articles = []
    skipped = 0
    failed = 0

    for idx, article in enumerate(raw_articles, start=1):
        try:
            processed = process_article(article)

            if processed:
                processed_articles.append(processed)
            else:
                skipped += 1

        except Exception as e:
            failed += 1
            print(f"[ERROR] Article #{idx}: {e}")

        if idx % 25 == 0:
            print(f"Processed {idx}/{len(raw_articles)}...")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            processed_articles,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("=" * 60)
    print("PROCESSING COMPLETE")
    print(f"Processed Successfully: {len(processed_articles)}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    print(f"Saved To: {OUTPUT_PATH}")
    print("Pipeline Version: phase_12_debugged_final")
    print("=" * 60)


if __name__ == "__main__":
    main()