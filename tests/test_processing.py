from nexlexhub.processing.chunker import semantic_chunk
from nexlexhub.processing.citation_extractor import extract_citations
from nexlexhub.processing.embedding_pipeline import generate_embedding
from nexlexhub.processing.metadata_extractor import extract_metadata


def test_semantic_chunking_and_metadata() -> None:
    text = (
        "Justice A delivered the judgment.\n\n"
        "Issue: whether Section 7 of the Insolvency and Bankruptcy Code applies.\n\n"
        "Held: the remedy is execution."
    )
    chunks = semantic_chunk(text, max_chars=80)
    assert chunks
    metadata = extract_metadata(text, "Example v. Example")
    assert metadata["legal_issues"]


def test_citation_extraction_and_embedding() -> None:
    text = "See (2019) 4 SCC 17 and Section 7 of the Insolvency and Bankruptcy Code."
    citations = extract_citations(text)
    assert len(citations) >= 2
    vector = generate_embedding(text)
    assert len(vector) == 16
