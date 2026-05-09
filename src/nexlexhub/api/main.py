from __future__ import annotations

from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.api.schemas import CaseOut, LegalAnalysisResponse, SearchRequest
from nexlexhub.core.config import get_settings
from nexlexhub.core.logging import configure_logging
from nexlexhub.core.security import require_role
from nexlexhub.db.session import SessionLocal, engine, get_db
from nexlexhub.services.bootstrap import seed_demo_data
from nexlexhub.services.legal_intelligence import (
    citations_index,
    graph_snapshot,
    legal_analysis,
    precedents_index,
    related_cases,
    search_cases,
    summary_counts,
    timeline,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    settings = get_settings()
    if settings.enable_demo_seed:
        async with SessionLocal() as session:
            await seed_demo_data(session)
    yield
    await engine.dispose()


app = FastAPI(title="NexLexHub Legal Intelligence API", version="2.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)) -> dict:
    await db.execute(text("SELECT 1"))
    return {"status": "ok", "service": "nexlexhub", "counts": await summary_counts(db)}


@app.post("/search", response_model=list[CaseOut], dependencies=[Depends(require_role("reader"))])
async def search(payload: SearchRequest, db: AsyncSession = Depends(get_db)) -> list[CaseOut]:
    cases = await search_cases(db, payload.query)
    return [CaseOut.model_validate(case, from_attributes=True) for case in cases[: payload.limit]]


@app.get("/cases", response_model=list[CaseOut], dependencies=[Depends(require_role("reader"))])
async def list_cases(db: AsyncSession = Depends(get_db)) -> list[CaseOut]:
    cases = await search_cases(db, "")
    return [CaseOut.model_validate(case, from_attributes=True) for case in cases]


@app.get("/citations", dependencies=[Depends(require_role("reader"))])
async def list_citations(db: AsyncSession = Depends(get_db)) -> list[dict]:
    return await citations_index(db)


@app.get("/precedents", dependencies=[Depends(require_role("reader"))])
async def list_precedents(db: AsyncSession = Depends(get_db)) -> list[dict]:
    return await precedents_index(db)


@app.post("/semantic-search", dependencies=[Depends(require_role("reader"))])
async def semantic_search(payload: SearchRequest, db: AsyncSession = Depends(get_db)) -> dict:
    return {"query": payload.query, "results": (await legal_analysis(db, payload.query))["results"]}


@app.post("/legal-analysis", response_model=LegalAnalysisResponse, dependencies=[Depends(require_role("analyst"))])
async def legal_analysis_endpoint(payload: SearchRequest, db: AsyncSession = Depends(get_db)) -> LegalAnalysisResponse:
    return LegalAnalysisResponse(**await legal_analysis(db, payload.query))


@app.get("/timeline", dependencies=[Depends(require_role("reader"))])
async def timeline_endpoint(db: AsyncSession = Depends(get_db)) -> list[dict]:
    return await timeline(db)


@app.get("/related-cases/{case_id}", dependencies=[Depends(require_role("reader"))])
async def related_cases_endpoint(case_id: int, db: AsyncSession = Depends(get_db)) -> list[dict]:
    return await related_cases(db, case_id)


@app.get("/graph", dependencies=[Depends(require_role("reader"))])
async def graph_endpoint(db: AsyncSession = Depends(get_db)) -> dict:
    return await graph_snapshot(db)


def run() -> None:
    uvicorn.run("nexlexhub.api.main:app", host="0.0.0.0", port=8000, reload=False)
