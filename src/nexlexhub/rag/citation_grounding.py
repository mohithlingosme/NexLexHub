from __future__ import annotations


def ground_answer(answer: str, citations: list[str]) -> dict[str, object]:
    return {
        "answer": answer,
        "citations": citations,
        "hallucination_risk": "low" if citations else "medium",
    }
