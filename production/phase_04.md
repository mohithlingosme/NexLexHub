⚖️ NexLexHub — Phase 4 Development Document
🏛️ Tribunal Expansion & Unified Legal Database
🚀 1. INTRODUCTION
1.1 What is Stage 4?

Stage 4 transforms NexLexHub into:

🏛️ A Unified Multi-Forum Legal Intelligence Platform

🎯 Core Objective

Integrate multiple tribunals into a single system:

Fragmented tribunal data → Unified searchable legal ecosystem
1.2 Tribunals Covered
National Company Law Tribunal (NCLT)
National Company Law Appellate Tribunal (NCLAT)
Income Tax Appellate Tribunal (ITAT)
Appellate Tribunal for Electricity (APTEL)
Customs, Excise and Service Tax Appellate Tribunal (CEGAT/CESTAT)
🔥 Key Upgrade
🌐 Cross-Forum Search
Search across all tribunals simultaneously
🧠 Unified Legal Database
Standardized schema for all judgments
🧠 2. SYSTEM ARCHITECTURE
High-Level Architecture
[Tribunal Sources]
      ↓
[Multi-Scraper Layer]
      ↓
[Parser + Normalizer]
      ↓
[Unified Schema Engine]
      ↓
[LLM Processing + Tagging]
      ↓
[Cross-Forum Indexing]
      ↓
[QA + Validation]
      ↓
[Unified Database]
      ↓
[Search + API + UI]
🔄 3. DATA PIPELINE
3.1 Input Sources

Each tribunal has:

Different formats
Different metadata structures
Different citation styles
3.2 Problem Solved

👉 Schema inconsistency

3.3 Solution
Unified Schema Design
{
  "case_id": "...",
  "forum": "NCLT / ITAT / etc",
  "title": "...",
  "bench": "...",
  "date": "...",
  "facts": "...",
  "issues": "...",
  "ratio": "...",
  "judgment": "...",
  "citations": [...]
}
🔍 4. PIPELINE STAGES
A. MULTI-SCRAPER ENGINE
🎯 Purpose

Handle multiple tribunal websites

Challenges:
Different layouts
Pagination differences
CAPTCHA / dynamic loading
Tech:
Playwright (dynamic scraping)
BeautifulSoup
Algorithms:
BFS (multi-page crawling)
Queue (URL management)
HashSet (deduplication)
B. PARSER + NORMALIZER
🎯 Purpose

Convert tribunal-specific formats into unified structure

Tasks:
Extract:
Case title
Bench
Date
Content
Algorithms:
Regex
Named Entity Recognition (NER)
DSA:
Trees (document structure)
C. UNIFIED SCHEMA ENGINE (CRITICAL)
🎯 Purpose

Standardize all tribunal data

Problem:

Each tribunal uses:

Different terminology
Different structure
Solution:

Map all fields into common schema

Algorithm:
Rule-based mapping
Ontology mapping
Example:
"Petitioner" → "Party A"
"Appellant" → "Party A"
D. LLM ENRICHMENT ENGINE
🎯 Purpose

Enhance tribunal data

Adds:
Summaries
Legal tags
Key issues
Algorithms:
Prompt engineering
Classification
🔗 E. CROSS-FORUM SEARCH ENGINE (KEY FEATURE)
🎯 Purpose

Search across all tribunals

Algorithms:
1. BM25 Ranking
Keyword-based search
2. Vector Search
Semantic search
3. Hybrid Search
Combine both
Flow:
Query → Keyword Search + Vector Search → Merge → Rank
DSA Used:
Inverted Index
Heaps (ranking)
🔄 F. CROSS-FORUM LINKING
🎯 Purpose

Link related cases across tribunals

Example:
ITAT case referencing Supreme Court
NCLT referencing NCLAT
Algorithms:
Graph-based linking
Cosine similarity
DSA:
Graph (nodes = cases, edges = references)
🧪 G. QA ENGINE
🎯 Purpose

Ensure:

Consistency across tribunals
Correct mapping
Checks:
Missing fields
Incorrect classification
📘 5. AI & ML SYSTEM
Models
Model	Purpose
BERT	Classification
GPT	Summarization
Sentence Transformer	Similarity
Graph Algorithms	Linking
ML Pipeline
Data → Train → Evaluate → Deploy → Monitor
🧠 6. ALGORITHMS USED
Task	Algorithm
Crawling	BFS
Parsing	Regex + NER
Schema mapping	Rule-based mapping
Search	BM25
Semantic search	Vector similarity
Linking	Graph algorithms
Ranking	Heap
Deduplication	MinHash
📦 7. DATA STORAGE DESIGN
PostgreSQL

Tables:

Cases
id
forum
title
date
Content
facts
issues
judgment
Cross-Links
case_id
related_case_id
ElasticSearch
Cross-forum search
Vector DB
Semantic retrieval
S3
PDFs
🔄 8. CRUD OPERATIONS
APIs:
GET /cases?forum=ITAT
GET /cases/search?q=...
GET /case/{id}
POST /case
PUT /case
DELETE /case
🎨 9. FRONTEND (UNIFIED UI)
Pages
🔍 Global Search Page
Search across all tribunals
Filters:
Forum
Date
Topic
📚 Case Page
Facts
Issues
Judgment
Forum tag
📊 Cross-Forum Graph View
Show relationships between cases
📊 10. ADMIN DASHBOARD
Features:
Tribunal-wise ingestion
Data consistency checks
Cross-link monitoring
Error logs
🔁 11. EVENT SYSTEM
Kafka Topics:
raw_tribunal_data
processed_cases
cross_links
🔐 12. SECURITY
JWT
RBAC
Secure APIs
🔍 13. SECURITY AUDIT
Data validation
Access control
API protection
🤖 14. ML VULNERABILITY SYSTEM
Detect incorrect mappings
Detect missing links
🔄 15. LIFECYCLE MANAGEMENT
Data:
Ingest → Normalize → Store
ML:
Train → Deploy → Monitor
🔁 16. CI/CD
Test
Deploy
Monitor
🧪 17. TESTING
Parser testing
Mapping validation
Search accuracy
🧰 18. INFRASTRUCTURE
Docker
Kubernetes
Terraform
📊 19. PERFORMANCE METRICS

Track:

Cases indexed
Search latency
Cross-link accuracy
Data consistency
🎯 20. FINAL EXECUTION FLOW
Scrape → Parse → Normalize → Enrich → Index → Link → QA → Store → Search → Display
