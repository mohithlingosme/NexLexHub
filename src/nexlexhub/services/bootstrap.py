from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.core.security import hash_password
from nexlexhub.db.models import (
    AIConversation,
    Alert,
    Case,
    Citation,
    Court,
    Embedding,
    Judgment,
    JudgmentChunk,
    LegalEvent,
    Precedent,
    Publisher,
    Statute,
    User,
)
from nexlexhub.processing.chunker import semantic_chunk
from nexlexhub.processing.citation_extractor import extract_citations
from nexlexhub.processing.embedding_pipeline import generate_embedding


async def seed_demo_data(session: AsyncSession) -> None:
    sc = await session.scalar(select(Court).where(Court.slug == "supreme-court"))
    if sc is None:
        sc = Court(name="Supreme Court", slug="supreme-court", level="apex", jurisdiction="India")
        session.add(sc)
    hc = await session.scalar(select(Court).where(Court.slug == "karnataka-high-court"))
    if hc is None:
        hc = Court(name="Karnataka High Court", slug="karnataka-high-court", level="high-court", jurisdiction="Karnataka")
        session.add(hc)
    ll = await session.scalar(select(Publisher).where(Publisher.name == "LiveLaw"))
    if ll is None:
        ll = Publisher(name="LiveLaw", homepage="https://www.livelaw.in")
        session.add(ll)
    bb = await session.scalar(select(Publisher).where(Publisher.name == "BarAndBench"))
    if bb is None:
        bb = Publisher(name="BarAndBench", homepage="https://www.barandbench.com")
        session.add(bb)
    admin = await session.scalar(select(User).where(User.email == "admin@nexlexhub.local"))
    if admin is None:
        admin = User(
            email="admin@nexlexhub.local",
            full_name="NexLexHub Admin",
            role="admin",
            password_hash=hash_password("admin123"),
            is_active=True,
        )
        session.add(admin)
    analyst = await session.scalar(select(User).where(User.email == "analyst@nexlexhub.local"))
    if analyst is None:
        analyst = User(
            email="analyst@nexlexhub.local",
            full_name="NexLexHub Analyst",
            role="analyst",
            password_hash=hash_password("analyst123"),
            is_active=True,
        )
        session.add(analyst)
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
    persisted_cases: list[Case] = []
    for case in cases:
        existing_case = await session.scalar(select(Case).where(Case.normalized_title == case.normalized_title))
        if existing_case is None:
            session.add(case)
            await session.flush()
            persisted_cases.append(case)
        else:
            persisted_cases.append(existing_case)
    for case in persisted_cases:
        if await session.scalar(select(Judgment.id).where(Judgment.case_id == case.id).limit(1)):
            continue
        base_text = f"{case.title}. {case.summary} Citation: {case.citation}. Section 7 of the Insolvency and Bankruptcy Code."
        session.add(
            Judgment(
                case_id=case.id,
                source_url=case.official_source_url,
                checksum=f"demo-{case.id}",
                mime_type="application/pdf",
                extracted_text=base_text,
                metadata_json={"source": "demo", "bench": case.metadata_json.get("bench", [])},
            )
        )
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
    if await session.scalar(select(Statute.id).limit(1)) is None:
        session.add_all(
            [
                Statute(
                    name="Insolvency and Bankruptcy Code, 2016",
                    citation="IBC Section 7",
                    source_url="https://www.indiacode.nic.in/",
                    metadata_json={"category": "insolvency"},
                ),
                Statute(
                    name="Motor Vehicles Act, 1988",
                    citation="MVA Section 66",
                    source_url="https://www.indiacode.nic.in/",
                    metadata_json={"category": "transport"},
                ),
            ]
        )
    if await session.scalar(select(Precedent.id).limit(1)) is None:
        session.add(
            Precedent(
                source_case_id=persisted_cases[0].id,
                cited_case_id=persisted_cases[1].id,
                cited_text=persisted_cases[1].citation or persisted_cases[1].title,
                treatment="distinguished",
            )
        )
    if await session.scalar(select(LegalEvent.id).limit(1)) is None:
        session.add(
            LegalEvent(
                headline="Supreme Court reiterates insolvency is not an execution shortcut",
                publisher_id=ll.id,
                source_url="https://events.nexlexhub.local/sc-insolvency-shortcut",
                court="Supreme Court",
                snippet="Event clustered from publisher metadata only.",
                entities=["Supreme", "Court", "Insolvency"],
                official_source_found=True,
                cluster_key="supreme-court-insolvency-execution",
                event_hash="evt-demo-1",
            )
        )
    if await session.scalar(select(Alert.id).limit(1)) is None:
        session.add(
            Alert(
                user=admin,
                name="IBC threshold alerts",
                query="section 7 insolvency execution",
                delivery_channel="email",
                metadata_json={"frequency": "daily"},
            )
        )
    if await session.scalar(select(AIConversation.id).limit(1)) is None:
        session.add(
            AIConversation(
                user=analyst,
                title="Threshold quashment research",
                query="Cases where investigation cannot be quashed at threshold",
                answer="Initial grounded demo answer.",
                sources_json=[{"citation": persisted_cases[0].citation, "case_id": persisted_cases[0].id}],
            )
        )
    await session.commit()
