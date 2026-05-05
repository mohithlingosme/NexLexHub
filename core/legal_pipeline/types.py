"""Pydantic models for Supreme Court Legal Pipeline."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, validator

from core.config import DEFAULT_CONFIG

class SupremeCourtCase(BaseModel):
    """Input case from Final_training_corpus.json."""
    model_config = ConfigDict(extra='allow')  # Flexible for JSON extras
    
    id: str = Field(..., description="Unique case ID")
    title: str = Field(..., description="Case title")
    content: str = Field(..., description="Raw case content")
    url: str = Field(..., description="Source URL")
    date: Optional[str] = Field(None, description="Date")
    source: Optional[str] = Field(None, description="Source e.g. BarAndBench")
    category_tags: Optional[List[str]] = Field(default_factory=list)
    
    @validator('content')
    def content_not_empty(cls, v):
        if not v or len(v.strip()) < 50:
            raise ValueError('Content too short')
        return v

class LegalBlogStructure(BaseModel):
    """Strict 8-section LLM output."""
    background_of_the_case: str = Field(..., description="Background")
    procedural_history: str = Field(..., description="Procedural History")
    courts_findings: str = Field(..., description="Court's Findings")
    key_legal_principles: List[str] = Field(..., description="Bullet points")
    statutory_framework: str = Field(..., description="Statutory Framework")
    important_precedents: List[str] = Field(..., description="Bullet points")
    final_ruling: str = Field(..., description="Final Ruling")
    conclusion: str = Field(..., description="Conclusion")
    
    @validator('*')
    def no_empty_sections(cls, v):
        if isinstance(v, str) and not v.strip():
            raise ValueError('Section cannot be empty')
        if isinstance(v, list) and not v:
            raise ValueError('Principles/Precedents cannot be empty')
        return v

class PipelineOutput(BaseModel):
    """Full pipeline result per case."""
    case: SupremeCourtCase
    structured: LegalBlogStructure
    html_content: str
    sql_insert: str
    search_results: Optional[List[str]] = None
    processed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

if __name__ == "__main__":
    # Test validation
    sample_case = SupremeCourtCase(
        id="test",
        title="Sample Case",
        content="Long content here..." * 20,
        url="https://example.com"
    )
    print("Valid case:", sample_case.model_dump_json(indent=2))

