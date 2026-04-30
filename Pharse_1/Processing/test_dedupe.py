import json
from pathlib import Path
from ScArticles_Redudancy_Remove import dedupe_articles, CONFIG  # Adjust import if needed

def test_basic_dedup():
    """Test basic duplicate removal"""
    test_data = [
        {"url": "http://test.com/1", "title": "Test Case 1", "content": "Content 1", "date": "2024-01-01"},
        {"url": "http://test.com/1", "title": "Test Case 1", "content": "Content 1", "date": "2024-01-01"},  # Dup URL
        {"url": "http://test.com/2", "title": "Test Case 2", "content": "Content 1", "date": "2024-01-02"},  # Dup content
    ]
    cleaned, stats = dedupe_articles(test_data)
    assert len(cleaned) == 2
    assert stats['url_duplicates'] == 1
    assert stats['content_exact'] == 1
    print("✅ Basic dedup passed")

def test_similarity():
    """Test title similarity"""
    test_data = [
        {"url": "http://a.com", "title": "UOI vs State important case", "content": "Unique", "date": "2024-01-01"},
        {"url": "http://b.com", "title": "UOI v State: Important case decision", "content": "Unique2", "date": "2024-01-01"},
    ]
    cleaned, stats = dedupe_articles(test_data)
    print(f"Similarity test stats: {stats}")

if __name__ == "__main__":
    test_basic_dedup()
    test_similarity()
    print("All tests passed!")
