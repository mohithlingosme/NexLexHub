"""Basic tests for legal pipeline."""

import pytest
import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

from core.legal_pipeline.types import SupremeCourtCase, LegalBlogStructure
from core.legal_pipeline.ollama_client import structure_case
from core.legal_pipeline.output_generators import generate_html

@pytest.fixture
def sample_case():
    return SupremeCourtCase(
        id="test1",
        title="Test Supreme Court Case",
        content="This is test case content with legal details. Background... procedural...",
        url="https://example.com/case",
        source="TestSource"
    )

def test_supreme_court_case_validation(sample_case):
    """Test case model."""
    assert sample_case.title == "Test Supreme Court Case"
    assert len(sample_case.content) > 50

@pytest.mark.asyncio
@patch('core.ai.llm_client.generate', new_callable=AsyncMock())
async def test_structure_case(mock_generate, sample_case):
    """Test LLM structuring."""
    mock_generate.return_value = json.dumps({
        "background_of_the_case": "Test background",
        "procedural_history": "Test history",
        "courts_findings": "Test findings",
        "key_legal_principles": ["principle 1", "principle 2"],
        "statutory_framework": "Test framework",
        "important_precedents": ["precedent 1"],
        "final_ruling": "Test ruling",
        "conclusion": "Test conclusion"
    })
    
    structured = await structure_case(sample_case, [])
    assert isinstance(structured, LegalBlogStructure)
    assert structured.background_of_the_case == "Test background"

def test_generate_html(sample_case):
    """Test HTML generation."""
    # Mock structured
    structured = LegalBlogStructure(
        background_of_the_case="bg",
        procedural_history="ph",
        courts_findings="cf",
        key_legal_principles=["p1"],
        statutory_framework="sf",
        important_precedents=["pre1"],
        final_ruling="fr",
        conclusion="con"
    )
    
    html = generate_html(structured, sample_case.title)
    assert "<h1>Test Supreme Court Case</h1>" in html
    assert "<ul>" in html

def test_sql_generation(sample_case):
    """Test SQL."""
    from core.legal_pipeline.output_generators import generate_sql
    structured = LegalBlogStructure(
        background_of_the_case="bg",
        procedural_history="ph'",  # Escapable
        courts_findings="cf",
        key_legal_principles=["p1"],
        statutory_framework="sf",
        important_precedents=["pre1"],
        final_ruling="fr",
        conclusion="con"
    )
    
    sql = generate_sql(sample_case, structured)
    assert "INSERT INTO supreme_court_cases" in sql
    assert "ph''" in sql  # Escaped single quote

if __name__ == "__main__":
    pytest.main(["-v"])

