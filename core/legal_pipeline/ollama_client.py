"""Specialized Ollama client for legal structuring."""

import json
from typing import List

from core.ai.llm_client import generate
from core.legal_pipeline.types import SupremeCourtCase, LegalBlogStructure

STRUCTURE_PROMPT = """
You are a senior Supreme Court analyst. Transform the following case into STRICT format:

# Supreme Court Cases

## Background of the Case
{raw_content}

## Procedural History

## Court's Findings

## Key Legal Principles (bullet points ONLY, min 3)

## Statutory Framework

## Important Precedents (bullet points ONLY, min 2)

## Final Ruling

## Conclusion

RULES (MANDATORY):
- EXACTLY these 8 sections, NO MORE NO LESS
- Formal legal tone
- Extract REAL insights from content
- Incorporate search context: {search_context}
- Principles/Precedents as markdown bullets
- No skipping sections even if data limited
- Comprehensive, 200-400 words per text section

Respond ONLY with JSON: {{"background_of_the_case": "...", "procedural_history": "...", ...}}
"""

async def structure_case(case: SupremeCourtCase, search_snippets: List[str]) -> LegalBlogStructure:
    """Generate structured blog via LLM."""
    context = "\n\n".join(search_snippets[:5]) if search_snippets else "No external context."
    
    prompt = STRUCTURE_PROMPT.format(
        raw_content=case.content[:4000],  # Truncate long content
        search_context=context,
    )
    
    response = await generate(prompt, model="llama3")
    
    try:
        structured_data = json.loads(response)
        return LegalBlogStructure(**structured_data)
    except (json.JSONDecodeError, ValueError) as e:
        # Fallback parsing or error
        raise ValueError(f"LLM output invalid: {e}. Raw: {response[:500]}")

if __name__ == "__main__":
    from core.legal_pipeline.types import SupremeCourtCase
    # Test stub
    case = SupremeCourtCase(id="test", title="Test", content="Test content...", url="")
    print("Ready for async test")

