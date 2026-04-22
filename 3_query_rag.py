#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


def _ensure_agent_on_path() -> None:
    here = Path(__file__).resolve().parent
    agent_root = here / "ai-legal-news-agent"
    if str(agent_root) not in sys.path:
        sys.path.insert(0, str(agent_root))


def main() -> int:
    _ensure_agent_on_path()
    from ai.rag import answer_with_context, retrieve

    parser = argparse.ArgumentParser(description="Query RAG store (no LangChain/FAISS).")
    parser.add_argument("--k", type=int, default=4, help="Top-k contexts to retrieve")
    args = parser.parse_args()

    print("Loading vector store from ai-legal-news-agent config...")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nAsk: ").strip()
        if query.lower() in ("exit", "quit"):
            break
        if not query:
            continue
        ctx = retrieve(query, k=args.k)
        ans = answer_with_context(query, ctx)
        print("\nAnswer:\n", ans)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

