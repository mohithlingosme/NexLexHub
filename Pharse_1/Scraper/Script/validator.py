"""Pydantic Schemas + Quality Validation.

Expanded LegalDocument w/ user-required fields.
Reject rules: generic titles, missing key fields, low confidence."""

import json
import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator, ConfigDict
from datetime import datetime

from config import config

logger = logging.getLogger(__name__)

class LegalDocument(BaseModel):
    model_config = ConfigDict(json_schema_extra={'required': ['title', 'source_hash']})
    
    source_hash: str = Field(..., description="Unique SHA256 hash")
    source_file: str
    source_url: str | None = None
    case_type: str | None = None
    court_name: str = Field(default="Supreme Court")
    bench: str | None = None
    judges: List[str] = Field(default_factory=list)
    decision_date: str | None = None
    citation_reference: str | None = None
    jurisdiction: str = "India"
    title: str
    facts: str
    procedural_history: str
    issues: List[str]
    findings: str
    statutes: List[str]
    precedents: List[str]
    final_ruling: str
    legal_significance: str
    seo_keywords: List[str] = Field(default_factory=list)
    seo_summary: str | None = None
    industry_domain: str | None = None
    document_type: str = "judgment"
    confidence_score: float = Field(ge=0.0, le=1.0)
    
    @validator('title')
    def reject_generic_title(cls, v):
        banned = config.banned_titles
        if any(b.lower() in v.lower() for b in banned):
            raise ValueError(f'Generic title banned: {v}')
        return v
    
    @validator('confidence_score')
    def check_min_conf(cls, v):
        if v < config.min_confidence:
            raise ValueError(f'Low confidence: {v}')
        return v

class AutomotiveDocument(BaseModel):
    # Future Autopredator schema
    source_hash: str
    source_file: str
    oem_specs: Dict[str, Any]
    variant_details: Dict[str, Any]
    pricing: Dict[str, Any]
    confidence_score: float

def validate_quality(doc: Dict[str, Any]) -> bool:
    """Reject malformed/generic."""
    try:
        LegalDocument.model_validate(doc)
        return True
    except Exception as e:
        logger.warning(f'Validation failed: {e}')
        return False

def register_source(hash_id: str, file_path: str, size: int, word_count: int):
    """Stub for source_registry INSERT (sql_exporter impl)."""
    logger.info(f'Registered source: {hash_id} ({word_count} words)')
    # Later: sqlite INSERT

