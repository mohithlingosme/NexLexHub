"""Main Pipeline Orchestrator.

Full production flow: ingest -> chunk -> Ollama extract -> validate -> SQL."""

import logging
import time
from pathlib import Path
from typing import List
import ollama
from rich.console import Console
from rich.progress import Progress

from config import config
from cleaner import ingest_bulk
from chunker import chunk_smart
from validator import LegalDocument, validate_quality
from sql_exporter import insert_documents

logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)
console = Console()

class OllamaExtractor:
    """Deterministic structured extraction w/ retry."""
    
    def __init__(self):
        self.schema = LegalDocument.model_json_schema()
    
    def build_prompt(self, chunk: str) -> str:
        """JSON-only prompt w/ schema grounding."""
        return f"""You are elite legal analyst. Extract ONLY from source.

SCHEMA (output JSON ONLY):
{json.dumps(self.schema, indent=2)}

SOURCE:
{chunk[:7000]}

Respond JSON ONLY. No generic titles."""
    
    def extract_chunk(self, chunk: str, retries: int = config.max_retries) -> List[Dict] | None:
        for attempt in range(retries):
            try:
                resp = ollama.chat(
                    model=config.model_name,
                    messages=[{'role': 'user', 'content': self.build_prompt(chunk)}],
                    format='json',
                    options={
                        'temperature': config.temperature,
                        'top_p': config.top_p,
                        'repeat_penalty': config.repeat_penalty,
                        'num_predict': config.num_predict
                    }
                )
                doc = LegalDocument.model_validate_json(resp['message']['content'])
                return [doc.model_dump()]
            except Exception as e:
                logger.warning(f'Extract retry {attempt+1}: {e}')
                time.sleep(2 ** attempt)
        return None

class PipelineOrchestrator:
    """Full resume-safe bulk processing."""
    
    def __init__(self):
        self.extractor = OllamaExtractor()
    
    def run(self):
        with Progress() as progress:
            task = progress.add_task('Processing...', total=None)
            
            # Ingest
            docs = ingest_bulk()
            progress.advance(task)
            
            all_extracted = []
            failed = []
            
            for doc in docs:
                chunks = chunk_smart(doc['cleaned_content'])
                extracted = []
                
                for chunk in chunks:
                    result = self.extractor.extract_chunk(chunk)
                    if result and validate_quality(result[0]):
                        extracted.extend(result)
                    else:
                        failed.append(doc['source_hash'])
                
                if extracted:
                    all_extracted.extend(extracted)
            
            # Export
            insert_documents(all_extracted)
            
            # Metrics
            console.print(f'[green]✅ {len(all_extracted)} docs processed[/]')
            console.print(f'[red]❌ {len(failed)} failed[/]')
            console.print(f'[blue]💾 SQLite: {config.sqlite_db}[/]')

if __name__ == '__main__':
    orchestrator = PipelineOrchestrator()
    orchestrator.run()

