import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter


# =========================================================
# CONFIG
# =========================================================

INPUT_PATH = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Cleaned data\Cleaned_Sc_articles.json"
)

OUTPUT_PATH = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Structured\Structured_SC_Blogs.json"
)

REJECTED_PATH = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Structured\Rejected_SC_Blogs.json"
)

REPORT_PATH = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Structured\SC_Blog_Report.json"
)

MIN_WORD_COUNT = 80


# =========================================================
# UTILITIES
# =========================================================

def normalize_text(text):
    """Clean whitespace and formatting."""
    if not text:
        return ""

    text = str(text)

    replacements = {
        "\n": " ",
        "\r": " ",
        "\t": " ",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "₹": "Rs.",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\.\.+', '.', text)

    return text.strip()


def generate_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)


# =========================================================
# FILTERING
# =========================================================

def reject_article(article):
    """
    Safe enterprise filtering without over-rejection
    """

    title = normalize_text(article.get("title", ""))
    content = normalize_text(article.get("content", ""))

    if not title:
        return True, "Missing title"

    if not content:
        return True, "Missing content"

    word_count = article.get("word_count", 0)

    if word_count == 0:
        word_count = len(content.split())

    if word_count < MIN_WORD_COUNT:
        return True, "Low word count"

    bad_terms = [
        "subscribe now",
        "click here",
        "advertisement",
        "sponsored content"
    ]

    lower_text = (title + " " + content).lower()

    for term in bad_terms:
        if term in lower_text:
            return True, f"Promotional content: {term}"

    return False, ""


# =========================================================
# EXTRACTION
# =========================================================

def extract_case_name(article):
    refs = article.get("case_references", [])

    valid_refs = [
        ref for ref in refs
        if " v. " in ref.lower() and len(ref) > 15
    ]

    return valid_refs[0] if valid_refs else "Unknown Case"


def generate_headline(article):
    title = normalize_text(article.get("title", ""))

    if "supreme court" not in title.lower():
        title = f"Supreme Court: {title}"

    return title


def generate_lead(article):
    sentences = split_sentences(article["content"])
    return normalize_text(" ".join(sentences[:3]))


def generate_background(article):
    sentences = split_sentences(article["content"])

    if len(sentences) > 8:
        return normalize_text(" ".join(sentences[3:8]))

    return normalize_text(" ".join(sentences[3:]))


def generate_conflict(article):
    content = article["content"]

    patterns = [
        r'High Court.*?\.',
        r'Magistrate.*?\.',
        r'lower court.*?\.',
        r'quashed.*?\.',
        r'set aside.*?\.'
    ]

    findings = []

    for pattern in patterns:
        matches = re.findall(pattern, content, flags=re.IGNORECASE)
        findings.extend(matches)

    return normalize_text(" ".join(findings[:5]))


def generate_analysis(article):
    sentences = split_sentences(article["content"])

    if len(sentences) > 20:
        analysis = " ".join(sentences[8:20])
    else:
        analysis = " ".join(sentences[8:])

    return normalize_text(analysis)


def extract_precedents(article):
    refs = article.get("case_references", [])
    legal_entities = article.get("legal_entities", [])

    precedents = []

    for ref in refs:
        if " v. " in ref.lower() and len(ref) > 15:
            precedents.append(ref)

    for entity in legal_entities:
        if any(term in entity.lower() for term in [
            "article", "bnss", "crpc", "constitution"
        ]):
            precedents.append(entity)

    return sorted(list(set(precedents)))


def generate_final_ruling(article):
    sentences = split_sentences(article["content"])

    if len(sentences) >= 5:
        ruling = " ".join(sentences[-5:])
    else:
        ruling = article["content"]

    return normalize_text(ruling)


# =========================================================
# LEGAL PRINCIPLE MAPPING
# =========================================================

def map_legal_principles(content):
    principles = []

    doctrine_map = {
        "Investigation vs Trial Distinction": [
            "investigation", "trial", "mini-trial"
        ],
        "Magistrate Gatekeeping Role": [
            "magistrate", "section 156", "section 175"
        ],
        "High Court Quashing Limits": [
            "high court", "quash", "482", "226"
        ],
        "Prima Facie Standard": [
            "prima facie"
        ],
        "Bail Jurisprudence": [
            "bail"
        ],
        "Corporate Criminal Liability": [
            "shareholder", "corporate", "director"
        ],
        "Constitutional Rights": [
            "article 14", "article 21", "fundamental rights"
        ]
    }

    lower = content.lower()

    for doctrine, keywords in doctrine_map.items():
        if any(keyword in lower for keyword in keywords):
            principles.append(doctrine)

    return principles


# =========================================================
# BLOG BUILDING
# =========================================================

def build_structured_blog(article):
    content = normalize_text(article["content"])

    structured = {
        "id": article.get("id"),
        "url": article.get("url"),
        "title": generate_headline(article),
        "author": article.get("author", ""),
        "source": article.get("source", ""),
        "court": article.get("court", ""),
        "date": article.get("date", ""),
        "case_name": extract_case_name(article),

        "lead_summary": generate_lead(article),

        "background_context": generate_background(article),

        "conflict_or_lower_court_error": generate_conflict(article),

        "supreme_court_analysis": generate_analysis(article),

        "precedents_and_authorities": extract_precedents(article),

        "legal_principles": map_legal_principles(content),

        "final_ruling": generate_final_ruling(article),

        "original_categories": article.get("category_tags", []),

        "seo_keywords": [
            "Supreme Court",
            "BNSS",
            "CrPC",
            "Indian Judiciary",
            "Legal News",
            article.get("court", "")
        ],

        "training_format": {
            "instruction":
                f"Summarize and analyze Supreme Court legal news: {article.get('title')}",

            "input":
                content,

            "output": {
                "headline": generate_headline(article),
                "lead": generate_lead(article),
                "background": generate_background(article),
                "analysis": generate_analysis(article),
                "precedents": extract_precedents(article),
                "legal_principles": map_legal_principles(content),
                "ruling": generate_final_ruling(article)
            }
        },

        "processed_at":
            datetime.now(timezone.utc).isoformat(),

        "pipeline_version":
            "nexlexhub_sc_pipeline_final_v1"
    }

    return structured


# =========================================================
# MAIN PIPELINE
# =========================================================

def process_pipeline():
    print("=" * 70)
    print("NexLexHub Supreme Court News Structuring Pipeline")
    print("=" * 70)

    if not INPUT_PATH.exists():
        print("ERROR: Input file not found.")
        return

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    accepted = []
    rejected = []

    seen_hashes = set()
    seen_urls = set()

    category_counter = Counter()

    for idx, article in enumerate(articles, start=1):
        try:
            url = article.get("url", "")
            content = normalize_text(article.get("content", ""))

            if not content:
                rejected.append({
                    "reason": "Empty content",
                    "article": article
                })
                continue

            if url in seen_urls:
                rejected.append({
                    "reason": "Duplicate URL",
                    "article": article
                })
                continue

            content_hash = generate_hash(content)

            if content_hash in seen_hashes:
                rejected.append({
                    "reason": "Duplicate content",
                    "article": article
                })
                continue

            seen_urls.add(url)
            seen_hashes.add(content_hash)

            reject, reason = reject_article(article)

            if reject:
                print(f"REJECTED: {article.get('title', 'Unknown')} --> {reason}")

                rejected.append({
                    "reason": reason,
                    "article": article
                })
                continue

            structured_blog = build_structured_blog(article)

            accepted.append(structured_blog)

            print(f"ACCEPTED: {article.get('title', 'Unknown')}")

            for cat in article.get("category_tags", []):
                category_counter[cat] += 1

            if idx % 25 == 0:
                print(f"Processed {idx}/{len(articles)} articles...")

        except Exception as e:
            rejected.append({
                "reason": str(e),
                "article": article
            })

    # =====================================================
    # SAVE OUTPUTS
    # =====================================================

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(accepted, f, indent=4, ensure_ascii=False)

    with open(REJECTED_PATH, "w", encoding="utf-8") as f:
        json.dump(rejected, f, indent=4, ensure_ascii=False)

    report = {
        "total_articles": len(articles),
        "accepted_articles": len(accepted),
        "rejected_articles": len(rejected),

        "acceptance_rate":
            round((len(accepted) / len(articles)) * 100, 2)
            if articles else 0,

        "category_distribution":
            dict(category_counter),

        "generated_at":
            datetime.now(timezone.utc).isoformat(),

        "pipeline_version":
            "nexlexhub_sc_pipeline_final_v1"
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    # =====================================================
    # FINAL REPORT
    # =====================================================

    print("=" * 70)
    print("PIPELINE COMPLETE")
    print(f"Accepted Articles : {len(accepted)}")
    print(f"Rejected Articles : {len(rejected)}")
    print(f"Acceptance Rate   : {report['acceptance_rate']}%")
    print(f"Structured Output : {OUTPUT_PATH}")
    print(f"Rejected Output   : {REJECTED_PATH}")
    print(f"Report Output     : {REPORT_PATH}")
    print("=" * 70)


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    process_pipeline()