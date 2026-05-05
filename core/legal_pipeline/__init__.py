"""Legal Supreme Court Pipeline package."""

from .types import SupremeCourtCase, LegalBlogStructure, PipelineOutput
from .web_search import search_case_context
from .ollama_client import structure_case
from .output_generators import generate_html, generate_sql, to_pipeline_output
from .processor import process_file
# from .config import DEFAULT_CONFIG  # Use core.config.DEFAULT_CONFIG

__all__ = [
    "SupremeCourtCase",
    "LegalBlogStructure", 
    "PipelineOutput",
    "search_case_context",
    "structure_case",
    "generate_html",
    "generate_sql",
    "to_pipeline_output",
    "process_file",
]

