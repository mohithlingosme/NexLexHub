"""Main pipeline orchestrator."""

import asyncio
import json
import logging
from pathlib import Path
from typing import List

from core.legal_pipeline.types import SupremeCourtCase, PipelineOutput
from core.legal_pipeline.web_search import search_case_context
from core.legal_pipeline.ollama_client import structure_case
from core.legal_pipeline.output_generators import generate_html, generate_sql, to_pipeline_output
from core.config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)

class LegalPipelineProcessor:
    """Batch processor."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.html_dir = output_dir / "html"
        self.sql_dir = output_dir / "sql"
        self.json_dir = output_dir / "json"
        for d in [self.html_dir, self.sql_dir, self.json_dir]:
            d.mkdir(exist_ok=True)
    
    async def process_single(self, case: SupremeCourtCase) -> PipelineOutput:
        """Process one case."""
        logger.info("Processing: %s", case.title)
        
        # Web search
        snippets = await search_case_context(case.title, case.content[:200])
        
        # Structure
        structured = await structure_case(case, snippets)
        
        # Generate outputs
        html = generate_html(structured, case.title)
        sql = generate_sql(case, structured)
        
        return to_pipeline_output(case, structured, html, sql, snippets)
    
    async def process_batch(self, cases: List[SupremeCourtCase], batch_size: int = 5) -> List[PipelineOutput]:
        """Batch process."""
        results = []
        semaphore = asyncio.Semaphore(batch_size)
        
        async def bounded_process(case):
            async with semaphore:
                return await self.process_single(case)
        
        tasks = [bounded_process(case) for case in cases]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter exceptions
        valid_results = [r for r in results if not isinstance(r, Exception)]
        if len(valid_results) < len(results):
            logger.warning("Some cases failed")
        
        return valid_results
    
    def save_outputs(self, result: PipelineOutput):
        """Save HTML/SQL/JSON per case."""
        safe_title = result.case.title.replace('/', '_').replace('\\', '_')[:100]
        
        # HTML
        html_path = self.html_dir / f"{safe_title}.html"
        html_path.write_text(result.html_content)
        
        # SQL
        sql_path = self.sql_dir / f"{safe_title}.sql"
        sql_path.write_text(result.sql_insert)
        
        # JSON
        json_path = self.json_dir / f"{safe_title}.json"
        json_path.write_text(result.model_dump_json(indent=2))
        
        logger.info("Saved: %s", safe_title)

async def process_file(json_path: Path, limit: int | None = None) -> List[PipelineOutput]:
    """Load JSON → process."""
    with open(json_path) as f:
        data = json.load(f)
    
    cases = [SupremeCourtCase.model_validate(item) for item in data[:limit or len(data)]]
    
    processor = LegalPipelineProcessor(Path(DEFAULT_CONFIG.legal_pipeline.output_dir))
    results = await processor.process_batch(cases)
    
    for result in results:
        processor.save_outputs(result)
    
    return results

if __name__ == "__main__":
    import sys
    asyncio.run(process_file(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("test.json")))

