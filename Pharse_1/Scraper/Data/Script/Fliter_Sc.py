import json
import re
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter


# =========================
# CONFIG
# =========================

INPUT_PATH = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Processed\Phase15_Enhanced_Legal_Corpus.json"
)

OUTPUT_INSTRUCTION = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\AI\Phase16_Legal_LLM_Instruction_Dataset.jsonl"
)

OUTPUT_QA = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\AI\Phase16_Legal_LLM_QA_Dataset.jsonl"
)

OUTPUT_RAG = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\AI\Phase16_RAG_Embeddings.json"
)

OUTPUT_MODELFILE = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\AI\Phase16_Ollama_Modelfile.txt"
)

OUTPUT_REPORT = Path(
    r"C:\Users\Admin\OneDrive\Documents\GitHub\NexLexHub\Pharse_1\AI\Phase16_Training_Report.json"
)


# =========================
# HELPERS
# =========================

def clean_text(text):
    if not text:
        return ""
    text = str(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def truncate_text(text, limit=6000):
    return text[:limit]


# =========================
# INSTRUCTION DATASET
# =========================

def build_instruction_sample(article):
    instruction = (
        f"Analyze the following Indian legal article and provide summary, "
        f"legal principles, doctrines, precedents, and practical implications."
    )

    input_text = truncate_text(article.get("content", ""))

    output = {
        "summary": article.get("summary", ""),
        "headnote": article.get("headnote", ""),
        "legal_principles": article.get("key_principles", []),
        "doctrines": article.get("doctrines", []),
        "precedents": article.get("precedents", []),
        "court": article.get("court", ""),
        "category_tags": article.get("category_tags", []),
        "legal_issues": article.get("legal_issues", [])
    }

    return {
        "instruction": instruction,
        "input": input_text,
        "output": output
    }


# =========================
# QA DATASET
# =========================

def build_qa_pairs(article):
    qa_pairs = []

    title = article.get("title", "")
    summary = article.get("summary", "")
    doctrines = article.get("doctrines", [])
    principles = article.get("key_principles", [])

    if summary:
        qa_pairs.append({
            "question": f"What is the summary of the case/article: {title}?",
            "answer": summary
        })

    if doctrines:
        qa_pairs.append({
            "question": f"What legal doctrines are involved in {title}?",
            "answer": ", ".join(doctrines)
        })

    if principles:
        qa_pairs.append({
            "question": f"What are the key legal principles in {title}?",
            "answer": ", ".join(principles)
        })

    return qa_pairs


# =========================
# RAG EMBEDDING RECORD
# =========================

def build_rag_record(article):
    searchable_text = " ".join([
        article.get("title", ""),
        article.get("summary", ""),
        article.get("content", "")[:5000],
        " ".join(article.get("category_tags", [])),
        " ".join(article.get("doctrines", [])),
        " ".join(article.get("key_principles", []))
    ])

    return {
        "id": article["id"],
        "title": article.get("title", ""),
        "embedding_text": clean_text(searchable_text),
        "court": article.get("court", ""),
        "date": article.get("date", ""),
        "categories": article.get("category_tags", []),
        "tier": article.get("tier", "")
    }


# =========================
# OLLAMA MODELFILE
# =========================

def generate_modelfile():
    return """
FROM llama3:8b

PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 8192

SYSTEM \"\"\"
You are NexLexHub Legal AI,
an advanced Indian legal research and corporate compliance assistant.

Capabilities:
- Indian constitutional law
- Supreme Court case analysis
- Corporate law
- Company law
- Taxation
- CS Executive preparation
- Legal drafting
- Compliance advisory
- Judicial precedent analysis

Always provide:
- Accurate legal analysis
- Structured summaries
- Relevant doctrines
- Corporate implications
- Practical legal application
\"\"\"
"""


# =========================
# MAIN PIPELINE
# =========================

def process_phase16():
    print("=" * 75)
    print("NexLexHub Phase 16 Complete Legal LLM Pipeline")
    print("=" * 75)

    if not INPUT_PATH.exists():
        print("Phase15 input missing.")
        return

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    OUTPUT_INSTRUCTION.parent.mkdir(parents=True, exist_ok=True)

    instruction_count = 0
    qa_count = 0
    rag_count = 0

    category_counter = Counter()
    doctrine_counter = Counter()

    rag_records = []

    # =========================
    # INSTRUCTION DATASET
    # =========================

    with open(OUTPUT_INSTRUCTION, "w", encoding="utf-8") as inst_f, \
         open(OUTPUT_QA, "w", encoding="utf-8") as qa_f:

        for idx, article in enumerate(articles, start=1):
            try:
                # Instruction sample
                instruction_sample = build_instruction_sample(article)
                inst_f.write(
                    json.dumps(instruction_sample, ensure_ascii=False) + "\n"
                )
                instruction_count += 1

                # QA pairs
                qa_pairs = build_qa_pairs(article)

                for qa in qa_pairs:
                    qa_f.write(
                        json.dumps(qa, ensure_ascii=False) + "\n"
                    )
                    qa_count += 1

                # RAG
                rag_record = build_rag_record(article)
                rag_records.append(rag_record)
                rag_count += 1

                # Analytics
                for cat in article.get("category_tags", []):
                    category_counter[cat] += 1

                for doctrine in article.get("doctrines", []):
                    doctrine_counter[doctrine] += 1

                if idx % 100 == 0:
                    print(f"Processed {idx}/{len(articles)} articles...")

            except Exception as e:
                print(f"Error processing article {idx}: {e}")

    # Save RAG corpus
    with open(OUTPUT_RAG, "w", encoding="utf-8") as f:
        json.dump(rag_records, f, indent=4, ensure_ascii=False)

    # Save Modelfile
    with open(OUTPUT_MODELFILE, "w", encoding="utf-8") as f:
        f.write(generate_modelfile())

    # Report
    report = {
        "total_articles": len(articles),
        "instruction_samples": instruction_count,
        "qa_pairs": qa_count,
        "rag_records": rag_count,
        "top_categories": dict(category_counter),
        "top_doctrines": dict(doctrine_counter),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pipeline_version": "phase_16_complete_legal_llm"
    }

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print("=" * 75)
    print("PHASE 16 COMPLETE")
    print(f"Instruction Dataset: {OUTPUT_INSTRUCTION}")
    print(f"QA Dataset: {OUTPUT_QA}")
    print(f"RAG Embeddings: {OUTPUT_RAG}")
    print(f"Ollama Modelfile: {OUTPUT_MODELFILE}")
    print(f"Training Report: {OUTPUT_REPORT}")
    print("=" * 75)

    print("\nNEXT DEPLOYMENT:")
    print("1. ollama create nexlexhub-legal -f Phase16_Ollama_Modelfile.txt")
    print("2. Fine-tune using LoRA/QLoRA")
    print("3. Deploy with vector DB (Chroma/FAISS/Qdrant)")
    print("4. Build NexLexHub Legal SaaS Interface")
    print("5. Add corporate compliance + CS Executive modules")


# =========================
# ENTRY
# =========================

if __name__ == "__main__":
    process_phase16()