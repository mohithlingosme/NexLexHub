import json
import re
import hashlib
import unicodedata
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

# =========================
# CONFIG
# =========================

INPUT_PATH = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Cleaned data\Cleaned_Sc_articles.json"
)

OUTPUT_CORPUS = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Filter\Supreme_Court\Final_training_corpus.json"
)

OUTPUT_REJECTED = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Filter\Supreme_Court\Rejected.json"
)

OUTPUT_REPORT = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Filter\Supreme_Court\report.json"
)

MIN_WORD_COUNT = 150
MIN_QUALITY_SCORE = 250


# =========================
# TEXT UTILITIES
# =========================

def normalize_unicode(text):
    if not text:
        return ""
    return unicodedata.normalize("NFKC", str(text))


def normalize_whitespace(text):
    text = normalize_unicode(text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\.\.+", ".", text)
    text = re.sub(r"\s+\.", ".", text)
    return text.strip()


def hash_text(text):
    return hashlib.sha256(
        normalize_whitespace(text).encode("utf-8")
    ).hexdigest()


# =========================
# CASE SANITIZATION
# =========================

def sanitize_case_references(case_refs):
    cleaned = []

    for ref in case_refs:
        ref = normalize_whitespace(ref)

        if (
            " v. " in ref
            and len(ref) > 15
            and len(ref) < 300
        ):
            ref = re.sub(r"^.*?(?=[A-Z])", "", ref)
            ref = re.sub(r"\.+$", "", ref)

            if ref not in cleaned:
                cleaned.append(ref)

    return cleaned


# =========================
# JUDGE SANITIZATION
# =========================

def sanitize_judges(judges):
    cleaned = []

    for judge in judges:
        judge = normalize_whitespace(judge)

        invalid_terms = [
            "said",
            "remarked",
            "approval",
            "pointed out",
            "application",
            "court",
            "bench"
        ]

        if any(term in judge.lower() for term in invalid_terms):
            continue

        if (
            judge.startswith("Justice")
            and len(judge.split()) <= 5
            and judge not in cleaned
        ):
            cleaned.append(judge)

    return cleaned


# =========================
# FILTERING
# =========================

def is_rejected(article):
    title = article.get("title", "").lower()
    content = article.get("content", "").lower()

    bad_title_terms = [
        "webinar", "subscribe", "advertisement",
        "sponsored", "editorial", "event",
        "job", "register", "opinion"
    ]

    bad_content_terms = [
        "sign up", "click here",
        "register now", "advertisement"
    ]

    if article.get("word_count", 0) < MIN_WORD_COUNT:
        return True, "Low word count"

    if not article.get("title") or not article.get("content"):
        return True, "Missing required fields"

    if any(term in title for term in bad_title_terms):
        return True, "Irrelevant title"

    if any(term in content for term in bad_content_terms):
        return True, "Promotional content"

    return False, ""


# =========================
# QUALITY SCORE
# =========================

def calculate_quality_score(article):
    score = 0

    score += min(article.get("word_count", 0), 2500)

    score += len(article.get("case_references", [])) * 25
    score += len(article.get("judges", [])) * 20
    score += len(article.get("legal_entities", [])) * 15
    score += article.get("chunk_count", 0) * 5
    score += len(article.get("category_tags", [])) * 10

    return score


# =========================
# SUMMARIZATION
# =========================

def generate_summary(content):
    content = normalize_whitespace(content)

    sentences = re.split(r'(?<=[.!?])\s+', content)

    cleaned_sentences = []

    for s in sentences:
        if len(s.split()) >= 8:
            cleaned_sentences.append(s)

    if len(cleaned_sentences) <= 5:
        return " ".join(cleaned_sentences[:5])[:3000]

    return " ".join(cleaned_sentences[:5])[:3000]


# =========================
# HEADNOTE
# =========================

def generate_headnote(article):
    return (
        f"{article.get('title', '')} | "
        f"Court: {article.get('court', '')} | "
        f"Categories: {', '.join(article.get('category_tags', []))}"
    )


# =========================
# LEGAL PRINCIPLES
# =========================

def extract_key_principles(content):
    principles = []

    patterns = [
        r'Article\s+\d+[A-Z]?',
        r'fundamental rights',
        r'bail',
        r'constitutional',
        r'insolvency',
        r'criminal liability',
        r'corporate governance',
        r'judicial review',
        r'natural justice'
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content, flags=re.IGNORECASE)

        for match in matches:
            match = normalize_whitespace(match)

            if match not in principles:
                principles.append(match)

    return principles


# =========================
# DOCTRINES
# =========================

def map_doctrines(content):
    doctrines = []

    doctrine_map = {
        "Natural Justice": ["natural justice", "fair hearing"],
        "Judicial Review": ["judicial review"],
        "Fundamental Rights": [
            "fundamental rights",
            "article 14",
            "article 21"
        ],
        "Corporate Liability": [
            "shareholder",
            "corporate",
            "investor"
        ],
        "Criminal Procedure": [
            "bail",
            "custody",
            "arrest",
            "bnss"
        ],
        "Religious Freedom": [
            "article 25",
            "religion",
            "temple"
        ]
    }

    lower_content = content.lower()

    for doctrine, keywords in doctrine_map.items():
        if any(keyword in lower_content for keyword in keywords):
            doctrines.append(doctrine)

    return doctrines


# =========================
# TRAINING FORMAT
# =========================

def generate_training_text(article, summary, principles, doctrines):
    return {
        "instruction":
            f"Summarize and analyze the legal article titled: {article['title']}",

        "input":
            article["content"],

        "output":
            {
                "summary": summary,
                "headnote": generate_headnote(article),
                "legal_principles": principles,
                "precedents": article.get("case_references", []),
                "doctrines": doctrines,
            }
    }


# =========================
# TIER CLASSIFICATION
# =========================

def classify_tier(score):
    if score >= 700:
        return "Tier_A"
    elif score >= 450:
        return "Tier_B"
    else:
        return "Tier_C"


# =========================
# MAIN PROCESSING
# =========================

def process_pipeline():
    print("=" * 70)
    print("NexLexHub Phase 14.1 Ultra Final Enterprise Pipeline")
    print("=" * 70)

    if not INPUT_PATH.exists():
        print("Input file missing.")
        return

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    accepted = []
    rejected = []

    seen_urls = set()
    seen_hashes = set()

    category_counter = Counter()

    total_articles = len(articles)

    for idx, article in enumerate(articles, start=1):
        try:
            url = article.get("url", "")
            content = normalize_whitespace(
                article.get("content", "")
            )

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

            content_hash = hash_text(content)

            if content_hash in seen_hashes:
                rejected.append({
                    "reason": "Duplicate Content",
                    "article": article
                })
                continue

            seen_urls.add(url)
            seen_hashes.add(content_hash)

            reject, reason = is_rejected(article)

            if reject:
                rejected.append({
                    "reason": reason,
                    "article": article
                })
                continue

            article["content"] = content

            article["case_references"] = sanitize_case_references(
                article.get("case_references", [])
            )

            article["judges"] = sanitize_judges(
                article.get("judges", [])
            )

            article["bench_strength"] = (
                str(len(article["judges"]))
                if article["judges"]
                else "Unknown"
            )

            quality_score = calculate_quality_score(article)

            if quality_score < MIN_QUALITY_SCORE:
                rejected.append({
                    "reason": "Low quality score",
                    "article": article
                })
                continue

            summary = generate_summary(content)

            principles = extract_key_principles(content)

            doctrines = map_doctrines(content)

            tier = classify_tier(quality_score)

            final_article = {
                **article,
                "quality_score": quality_score,
                "tier": tier,
                "summary": summary,
                "headnote": generate_headnote(article),
                "key_principles": principles,
                "precedents": article.get("case_references", []),
                "doctrines": doctrines,
                "training_format": generate_training_text(
                    article,
                    summary,
                    principles,
                    doctrines
                ),
                "phase_14_processed_at":
                    datetime.now(timezone.utc).isoformat(),
                "pipeline_version":
                    "phase_14_1_ultra_final"
            }

            accepted.append(final_article)

            for cat in article.get("category_tags", []):
                category_counter[cat] += 1

            if idx % 50 == 0:
                print(
                    f"Processed {idx}/{total_articles} articles..."
                )

        except Exception as e:
            rejected.append({
                "reason": str(e),
                "article": article
            })

    # =========================
    # SAVE OUTPUTS
    # =========================

    OUTPUT_CORPUS.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_CORPUS, "w", encoding="utf-8") as f:
        json.dump(
            accepted,
            f,
            indent=4,
            ensure_ascii=False
        )

    with open(OUTPUT_REJECTED, "w", encoding="utf-8") as f:
        json.dump(
            rejected,
            f,
            indent=4,
            ensure_ascii=False
        )

    report = {
        "total_input_articles": total_articles,
        "accepted_articles": len(accepted),
        "rejected_articles": len(rejected),
        "acceptance_rate":
            round(
                (len(accepted) / total_articles) * 100,
                2
            ) if total_articles else 0,
        "average_quality_score":
            round(
                sum(
                    a["quality_score"]
                    for a in accepted
                ) / len(accepted),
                2
            ) if accepted else 0,
        "tier_distribution":
            dict(
                Counter(
                    a["tier"]
                    for a in accepted
                )
            ),
        "category_distribution":
            dict(category_counter),
        "generated_at":
            datetime.now(timezone.utc).isoformat(),
        "pipeline_version":
            "phase_14_1_ultra_final"
    }

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("=" * 70)
    print("PHASE 14.1 COMPLETE")
    print(f"Accepted Articles: {len(accepted)}")
    print(f"Rejected Articles: {len(rejected)}")
    print(f"Final Corpus: {OUTPUT_CORPUS}")
    print(f"Rejected Data: {OUTPUT_REJECTED}")
    print(f"Analytics Report: {OUTPUT_REPORT}")
    print("=" * 70)


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    process_pipeline()