NexLexHub: System Architecture & ML Engineering Design

Version: 1.0  |  Target: Production-Grade Legal AI Platform

This document outlines the architectural blueprint for a highly scalable, ML-driven legal data platform. It bridges data ingestion (scraping), deep learning (NLP/LLMs), and high-performance retrieval (RAG).

1. Data Structures & Algorithms (DSA)

Choosing the right DSA prevents bottlenecks when your dataset scales to millions of legal documents.

Component

Optimal Data Structure / Algorithm

Justification for Legal Tech

Deduplication

MinHash & LSH (Locality-Sensitive Hashing)

Scrapers often pull the same case from LiveLaw and Bar&Bench with slightly varied wording. MinHash detects near-duplicates in $O(1)$ time, saving expensive LLM processing costs.

Scraping Queue

Priority Queues (via Redis)

Supreme Court judgments need faster processing than lower court interim orders. Priority queues ensure high-value data is routed to ML workers first.

Text Chunking

Sliding Window with Semantic Boundaries

Legal documents cannot be split randomly. Using a sliding window algorithm that looks for natural breaks (e.g., newline \n\n or regex matching Section \d+) ensures legal context isn't severed mid-sentence.

Vector Search

HNSW (Hierarchical Navigable Small World)

The underlying algorithm in modern vector databases. It organizes embeddings into a multi-layered graph, allowing sub-millisecond similarity search across millions of dense vectors.

2. Vector Database Design

For legal Retrieval-Augmented Generation (RAG), pure semantic search is insufficient. If a user searches for "Section 438 CrPC", the system must find exact keyword matches, not just "conceptually similar" bail statutes.

Recommendation: Qdrant (or Pinecone as a fully-managed alternative)

Why Qdrant? It natively supports Hybrid Search (combining Dense vectors for semantics + Sparse vectors/BM25 for exact keyword matching). It is written in Rust, handles massive scale, and has exceptional payload (metadata) filtering.

2.1 Embedding Workflow

Semantic Chunking: Text is split into overlapping chunks of ~500 tokens.

Dual-Embedding: * Dense: Passed through an embedding model (e.g., text-embedding-3-small or InLegalBERT) to capture meaning.

Sparse: Processed via SPLADE or BM25 to capture exact legal terminologies.

Upsertion: Both vectors + metadata are batched and pushed to Qdrant.

2.2 Vector Schema Design

{
  "id": "UUID (e.g., hash of url + chunk_index)",
  "vector": {
    "dense": [0.015, -0.022, ...], // 1536 dimensions
    "sparse": { "indices": [14, 56], "values": [0.8, 0.4] } 
  },
  "payload": {
    "case_id": "SC-2026-1042",
    "court": "Supreme Court of India",
    "date": "2026-04-24",
    "chunk_index": 2,
    "text_content": "The bench quashed the FIR stating...",
    "source_url": "https://..."
  }
}


3. Data Management System (The Pipeline)

A robust pipeline decouples ingestion from processing to ensure that if the LLM API goes down, the scrapers don't crash.

Ingestion (Scrapers): Python scrapers (LiveLaw/SC) run asynchronously. They push raw JSON payloads into a Kafka or Redis/RabbitMQ message broker.

Object Storage (Raw Data): Raw HTML/JSON is saved immediately to Amazon S3 / MinIO. Never lose the raw data.

Processing Workers (Celery): * Worker pulls a message from the queue.

Cleans HTML and runs MinHash deduplication.

Sends text to local InLegalBERT for classification (Is this a judgment, news, or interim order?).

Structured Storage: Metadata (Title, Date, Court) is saved to a Relational Database (PostgreSQL).

Retrieval API: A FastAPI backend serves the PHP frontend. When a user searches, FastAPI queries PostgreSQL (for exact filters like Date) and Qdrant (for semantic text).

4. ML Integration & Feedback Loops

Machine Learning is integrated as microservices, not monolithic scripts.

4.1 Inference Architecture

Classification (InLegalBERT): Hosted locally using TorchServe or exported to ONNX format for high-speed, CPU-friendly inference.

Extraction/Summarization (LLM): The system passes the chunked text to an LLM (e.g., DeepSeek-R1 or OpenAI) with a strict system prompt to enforce your 8-point schema (Background, Reasoning, Ruling, etc.). Output is forced into JSON format.

4.2 The Feedback Loop (RLHF Pipeline)

Frontend Interaction: A lawyer reads an AI summary and clicks a "Thumbs Down" or edits a hallucinated fact.

Storage: This correction is saved to a model_feedback table in PostgreSQL.

Retraining/Fine-tuning: Once a month, an automated Airflow job exports this corrected data to fine-tune a smaller, localized model (like Llama-3-8B), gradually reducing reliance on expensive closed-source APIs.

5. System Architecture Diagram

[ LiveLaw / Bar&Bench ] 
         | (Scraping via Selenium/BeautifulSoup)
         v
+-----------------------+      +-------------------+
|   Ingestion Engine    | ---> | S3 / MinIO Bucket | (Raw HTML Archive)
| (Python + AsyncIO)    |      +-------------------+
+-----------------------+
         | (Push Raw JSON)
         v
[ Message Broker: Redis / RabbitMQ / Kafka ]
         |
         v
+-----------------------+      +-------------------------+
|  Celery ML Workers    | ---> | Local: InLegalBERT      | (Classification)
|  (Data Processing)    | ---> | External: LLM API       | (8-Point Summary)
+-----------------------+      +-------------------------+
         |
         | (Split outputs)
         |
  +------+-------+
  |              |
  v              v
[PostgreSQL]   [Qdrant / Pinecone]
(Relational)   (Vector Database)
(Users/Meta)   (Embeddings/Text)
  ^              ^
  |              |
  +------+-------+
         |
+-----------------------+
|  FastAPI Backend      | (Search, Auth, RAG Orchestration)
+-----------------------+
         | (REST APIs / JSON)
         v
[ PHP / JS Frontend ]


6. Best Practices & Bottleneck Mitigation

Potential Bottlenecks

API Rate Limits: Scraping fast but hitting LLM rate limits.

Solution: Implement Exponential Backoff in your Celery workers. Use a token bucket algorithm to throttle outgoing LLM requests.

Stale Scraper Selectors: DOM structures change, breaking scrapers.

Solution: Implement anomaly detection. If a scraper returns 0 articles for 24 hours, fire an alert to a Slack/Discord webhook.

Database Memory Leaks: Unbounded vector search can consume massive RAM.

Solution: Enable Scalar Quantization in Qdrant to compress vectors by up to 64x with negligible accuracy loss.

Reliability Mandates

Idempotency: Ensure the pipeline can safely re-process the same article twice without creating duplicate database entries (use unique hashes as Primary Keys).

Schema Evolution: LLM schemas change. Use Pydantic models in FastAPI to strictly validate the LLM's JSON output before it touches PostgreSQL. If the LLM hallucinates a bad JSON structure, catch it in the worker and retry.