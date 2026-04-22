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
    from ai.embed import build_vector_store

    parser = argparse.ArgumentParser(description="Build vector store (no LangChain/FAISS).")
    parser.add_argument("--limit", type=int, default=None, help="Optional max chunks to index")
    args = parser.parse_args()

    try:
        out = build_vector_store(limit=args.limit)
    except FileNotFoundError as exc:
        print(f"Missing chunks: {exc}")
        print("Run: `python ai-legal-news-agent/main.py full` (or at least `chunk`) first.")
        return 1

    print(f"Vector store saved: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

