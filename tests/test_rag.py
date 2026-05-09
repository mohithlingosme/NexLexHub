from nexlexhub.rag.citation_grounding import ground_answer
from nexlexhub.rag.query_expansion import expand_query
from nexlexhub.rag.reranker import rerank


def test_rag_utilities() -> None:
    expanded = expand_query("section 7 insolvency")
    assert len(expanded) == 3
    reranked = rerank([{"score": 0.1}, {"score": 0.9}])
    assert reranked[0]["score"] == 0.9
    grounded = ground_answer("answer", ["(2019) 4 SCC 17"])
    assert grounded["hallucination_risk"] == "low"
