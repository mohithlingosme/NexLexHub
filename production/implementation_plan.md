# Implementation Plan for LexNexHub Phase 1 Documentation Refactor

## Overview
Convert the raw specification in 'production/pharse 1' into a comprehensive, actionable deep implementation blueprint preserving all sections (objectives, workflow, pipeline, architecture, security/ML vuln detection) while enhancing structure, schemas, diagrams, and checklists for developer execution. This creates a maintainable single source of truth aligned with ai-legal-news-agent codebase.

## Types
- **ArticleRaw**: { \"type\": \"object\", \"properties\": { \"url\": {\"type\": \"string\"}, \"title\": {\"type\": \"string\"}, \"content\": {\"type\": \"string\"}, \"date\": {\"type\": \"string\"}, \"category\": {\"type\": \"string\"}, \"scraped_at\": {\"type\": \"string\"} }, \"required\": [\"url\",\"title\",\"content\"] }
- **ProcessedArticle**: { \"type\": \"object\", \"properties\": { \"title\": {\"type\": \"string\"}, \"summary_intro\": {\"type\": \"string\"}, \"background\": {\"type\": \"string\"}, \"court_reasoning\": {\"type\": \"string\"}, \"legal_principles\": {\"type\": \"string\"}, \"case_references\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}}, \"final_ruling\": {\"type\": \"string\"}, \"conclusion\": {\"type\": \"string\"}, \"qa_score\": {\"type\": \"number\"}, \"tags\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}} }, \"required\": [\"title\",\"summary_intro\",\"background\",\"final_ruling\"] }
- **SecurityEvent**: { \"type\": \"object\", \"properties\": { \"type\": {\"type\": \"string\", \"enum\": [\"anomaly\",\"attack\",\"drift\"]}, \"risk_score\": {\"type\": \"number\"}, \"timestamp\": {\"type\": \"string\"}, \"details\": {\"type\": \"object\"} } }

## Files
- Modify: production/pharse 1 (full structured rewrite).
- New: None.

## Functions
Pseudocode:
- scrape_multi_source(sources: List[str]) -> List[ArticleRaw]
- llm_process(chunk: str) -> ProcessedArticle
- qa_validate(article: ProcessedArticle) -> float
- vulnerability_detect(logs: List[str]) -> List[SecurityEvent]

## Classes
- ScraperManager: crawl(), dedup_urls()
- PipelineRunner: qa_engine(), security_scan()
- MLVulnDetector: fit(), predict_risk()
- LegalContentType: Enum(News, Explanation, Insight, Newsletter)

## Dependencies
Add to requirements.txt: scikit-learn==1.5.0, pydantic==2.8.0, fastapi==0.115.0, celery==5.4.0, kafka-python==2.0.2

## Testing
Extend tests/test_pipeline.py with schema asserts, E2E runs, anomaly injection.

## Implementation Order
1. Refactor production/pharse 1
2. Validate Markdown
3. Update TODO.md
4. Complete
