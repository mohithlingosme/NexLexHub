import json
from pprint import pprint

# import functions from your main script
from Journalism_Agen.process_articles import (
    build_prompt,
    generate_with_retry,
    generate_html
)

INPUT_FILE = "articles.json"


# =========================
# 🧪 LOAD SAMPLE DATA
# =========================
def load_sample(n=1):
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data[:n]  # take first n articles


# =========================
# 🧪 TEST ONE ARTICLE
# =========================
def test_article(article):
    print("\n" + "="*60)
    print("🧪 TESTING ARTICLE:")
    print("Title:", article.get("title"))
    print("="*60)

    prompt = build_prompt(article)

    print("\n📨 PROMPT SENT (truncated):")
    print(prompt[:500], "...")

    # ✅ directly get structured JSON
    structured = generate_with_retry(prompt)

    if not structured:
        print("\n❌ FAILED: No valid JSON")
        return

    print("\n✅ STRUCTURED OUTPUT:")
    print(json.dumps(structured, indent=2)[:1500])

    html = generate_html({**structured, "date": article.get("date")})

    print("\n🌐 HTML PREVIEW:")
    print(html[:1000])

    print("\n✅ TEST SUCCESS")


# =========================
# 🚀 MAIN TEST
# =========================
def main():
    print("🚀 Running Test Pipeline...\n")

    sample_articles = load_sample(n=2)  # test 2 articles

    for article in sample_articles:
        test_article(article)

    print("\n🎉 ALL TESTS COMPLETED")


if __name__ == "__main__":
    main()
