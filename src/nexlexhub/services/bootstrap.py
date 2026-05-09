from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.db.models import Case, Citation, Court, Embedding, JudgmentChunk, Precedent, Publisher
from nexlexhub.processing.chunker import semantic_chunk
from nexlexhub.processing.citation_extractor import extract_citations
from nexlexhub.processing.embedding_pipeline import generate_embedding


async def seed_demo_data(session: AsyncSession) -> None:
    existing = await session.scalar(select(Case.id).limit(1))
    if existing:
        return
    sc = Court(name="Supreme Court", slug="supreme-court", level="apex", jurisdiction="India")
    hc = Court(name="Karnataka High Court", slug="karnataka-high-court", level="high-court", jurisdiction="Karnataka")
    ll = Publisher(name="LiveLaw", homepage="https://www.livelaw.in")
    bb = Publisher(name="BarAndBench", homepage="https://www.barandbench.com")
    session.add_all([sc, hc, ll, bb])
    await session.flush()
    cases = [
        Case(
            title="Anjani Technoplast Ltd. v. Shubh Gautam",
            normalized_title="anjani technoplast ltd v shubh gautam",
            case_number="CIVIL APPEAL No. 418/2026",
            citation="2026 LiveLaw (SC) 418",
            court_id=sc.id,
            publisher_id=ll.id,
            summary="IBC cannot be used as a substitute for execution proceedings against a solvent company.",
            ratio_decidendi="The insolvency mechanism cannot replace ordinary execution proceedings.",
            procedural_posture="appeal allowed",
            official_source_found=True,
            official_source_url="https://main.sci.gov.in/judgments/2026-livelaw-sc-418",
            decision_date=date(2026, 4, 23),
            legal_issues=["insolvency", "execution"],
            metadata_json={"bench": ["Justice P.S. Narasimha", "Justice Alok Aradhe"]},
        ),
        Case(
            title="State of Karnataka v. ANI Technologies",
            normalized_title="state of karnataka v ani technologies",
            case_number="SLP No. 1024/2026",
            citation="2026 LiveLaw (SC) 580",
            court_id=sc.id,
            publisher_id=bb.id,
            summary="Bike taxi regulation dispute on whether motorcycles may receive taxi permits.",
            ratio_decidendi="A blanket prohibition on bike taxis may offend Article 19(1)(g).",
            procedural_posture="special leave petition filed",
            official_source_found=False,
            legal_issues=["constitutional", "transport"],
            decision_date=date(2026, 5, 1),
            metadata_json={"bench": ["Justice Vibhu Bakhru", "Justice C.M. Joshi"]},
        ),
    ]
    session.add_all(cases)
    await session.flush()
    for case in cases:
        base_text = f"{case.title}. {case.summary} Citation: {case.citation}. Section 7 of the Insolvency and Bankruptcy Code."
        chunks = semantic_chunk(base_text)
        for chunk in chunks:
            chunk_row = JudgmentChunk(
                case_id=case.id,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
                section_tag=chunk.section_tag,
                paragraph_numbers=chunk.paragraph_numbers,
                metadata_json={"source": "demo"},
            )
            session.add(chunk_row)
            await session.flush()
            session.add(
                Embedding(
                    chunk_id=chunk_row.id,
                    provider="hash",
                    vector=generate_embedding(chunk.text),
                    bm25_hint=0.0,
                )
            )
            for citation in extract_citations(chunk.text):
                session.add(
                    Citation(
                        case_id=case.id,
                        chunk_id=chunk_row.id,
                        raw_text=citation["raw_text"],
                        normalized_text=citation["normalized_text"],
                        citation_type=citation["citation_type"],
                        verified=True,
                        source_url=case.official_source_url,
                    )
                )
    session.add(
        Precedent(
            source_case_id=cases[0].id,
            cited_case_id=cases[1].id,
            cited_text=cases[1].citation or cases[1].title,
            treatment="distinguished",
        )
    )
    await session.commit()
