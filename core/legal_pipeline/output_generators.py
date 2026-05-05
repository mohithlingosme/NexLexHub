"""HTML and SQL output generators."""

from datetime import datetime
from typing import List

from core.legal_pipeline.types import SupremeCourtCase, LegalBlogStructure, PipelineOutput

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Georgia, serif; max-width: 800px; margin: auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 8px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <h2>Background of the Case</h2>
    <p>{background}</p>
    
    <h2>Procedural History</h2>
    <p>{procedural}</p>
    
    <h2>Court's Findings</h2>
    <p>{findings}</p>
    
    <h2>Key Legal Principles</h2>
    <ul>{principles}</ul>
    
    <h2>Statutory Framework</h2>
    <p>{statutory}</p>
    
    <h2>Important Precedents</h2>
    <ul>{precedents}</ul>
    
    <h2>Final Ruling</h2>
    <p>{ruling}</p>
    
    <h2>Conclusion</h2>
    <p>{conclusion}</p>
</body>
</html>"""

def generate_html(structured: LegalBlogStructure, title: str) -> str:
    """Semantic HTML from structure."""
    principles_html = "".join(f"<li>{p}</li>" for p in structured.key_legal_principles)
    precedents_html = "".join(f"<li>{p}</li>" for p in structured.important_precedents)
    
    return HTML_TEMPLATE.format(
        title=title,
        background=structured.background_of_the_case.replace('\n', '<br>'),
        procedural=structured.procedural_history.replace('\n', '<br>'),
        findings=structured.courts_findings.replace('\n', '<br>'),
        principles=principles_html,
        statutory=structured.statutory_framework.replace('\n', '<br>'),
        precedents=precedents_html,
        ruling=structured.final_ruling.replace('\n', '<br>'),
        conclusion=structured.conclusion.replace('\n', '<br>')
    )

def generate_sql(case: SupremeCourtCase, structured: LegalBlogStructure) -> str:
    """Escaped SQL INSERT."""
    principles_json = json.dumps(structured.key_legal_principles)
    precedents_json = json.dumps(structured.important_precedents)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    # Simple escaping (use params in prod)
    def escape(s: str) -> str:
        return s.replace("'", "''").replace("\\", "\\\\")
    
    return f"""INSERT INTO supreme_court_cases (
        title, background, procedural_history, findings, principles, 
        statutory_framework, precedents, final_ruling, conclusion, created_at
    ) VALUES (
        '{escape(case.title)}',
        '{escape(structured.background_of_the_case)}',
        '{escape(structured.procedural_history)}',
        '{escape(structured.courts_findings)}',
        '{principles_json}',
        '{escape(structured.statutory_framework)}',
        '{precedents_json}',
        '{escape(structured.final_ruling)}',
        '{escape(structured.conclusion)}',
        '{now}'
    );"""

def to_pipeline_output(case: SupremeCourtCase, structured: LegalBlogStructure, html: str, sql: str, search_results: List[str] | None = None) -> PipelineOutput:
    """Convenience factory."""
    return PipelineOutput(
        case=case,
        structured=structured,
        html_content=html,
        sql_insert=sql,
        search_results=search_results
    )

