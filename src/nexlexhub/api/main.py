from __future__ import annotations

import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from nexlexhub.api.schemas import (
    AlertOut,
    CaseOut,
    ChatRequest,
    ConversationOut,
    LegalAnalysisResponse,
    LoginRequest,
    SearchRequest,
    StatuteOut,
    TokenResponse,
)
from nexlexhub.core.config import get_settings
from nexlexhub.core.logging import configure_logging
from nexlexhub.core.security import create_access_token, require_role, verify_password
from nexlexhub.db.models import User
from nexlexhub.db.session import SessionLocal, engine, get_db, init_models
from nexlexhub.services.bootstrap import seed_demo_data
from nexlexhub.services.legal_intelligence import (
    alerts_index,
    citations_index,
    conversations_index,
    create_conversation,
    graph_snapshot,
    legal_analysis,
    precedents_index,
    related_cases,
    search_cases,
    search_statutes,
    summary_counts,
    timeline,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    settings = get_settings()
    if settings.auto_init_db:
        await init_models()
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


@app.post("/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = await db.scalar(select(User).where(User.email == payload.email, User.is_active.is_(True)))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email, user.role), role=user.role)


@app.post("/search", response_model=list[CaseOut], dependencies=[Depends(require_role("reader"))])
async def search(payload: SearchRequest, db: AsyncSession = Depends(get_db)) -> list[CaseOut]:
    cases = await search_cases(db, payload.query)
    return [CaseOut.model_validate(case, from_attributes=True) for case in cases[: payload.limit]]


@app.post("/semantic-search", dependencies=[Depends(require_role("reader"))])
async def semantic_search(payload: SearchRequest, db: AsyncSession = Depends(get_db)) -> dict:
    analysis = await legal_analysis(db, payload.query)
    return {"query": payload.query, "results": analysis["results"], "grounding": analysis["grounding"]}


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


@app.get("/statutes", response_model=list[StatuteOut], dependencies=[Depends(require_role("reader"))])
async def list_statutes(query: str = "", db: AsyncSession = Depends(get_db)) -> list[StatuteOut]:
    statutes = await search_statutes(db, query)
    return [StatuteOut.model_validate(statute, from_attributes=True) for statute in statutes]


@app.get("/timeline", dependencies=[Depends(require_role("reader"))])
async def timeline_endpoint(db: AsyncSession = Depends(get_db)) -> list[dict]:
    return await timeline(db)


@app.post("/legal-analysis", response_model=LegalAnalysisResponse, dependencies=[Depends(require_role("analyst"))])
async def legal_analysis_endpoint(payload: SearchRequest, db: AsyncSession = Depends(get_db)) -> LegalAnalysisResponse:
    return LegalAnalysisResponse(**await legal_analysis(db, payload.query))


@app.post("/ai/chat", dependencies=[Depends(require_role("analyst"))])
async def chat(payload: ChatRequest, db: AsyncSession = Depends(get_db)) -> StreamingResponse:
    analysis = await legal_analysis(db, payload.query)
    summary = str(analysis["grounding"]["answer"])
    sources = analysis["results"][:3]
    await create_conversation(db, payload.query, summary, sources, payload.title)

    async def event_stream():
        for token in summary.split():
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield f"data: {json.dumps({'done': True, 'sources': sources})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/ai/conversations", response_model=list[ConversationOut], dependencies=[Depends(require_role("analyst"))])
async def ai_conversations(db: AsyncSession = Depends(get_db)) -> list[ConversationOut]:
    conversations = await conversations_index(db)
    return [ConversationOut.model_validate(conversation, from_attributes=True) for conversation in conversations]


@app.get("/alerts", response_model=list[AlertOut], dependencies=[Depends(require_role("reader"))])
async def alerts_endpoint(db: AsyncSession = Depends(get_db)) -> list[AlertOut]:
    alerts = await alerts_index(db)
    return [AlertOut.model_validate(alert, from_attributes=True) for alert in alerts]


@app.get("/related-cases/{case_id}", dependencies=[Depends(require_role("reader"))])
async def related_cases_endpoint(case_id: int, db: AsyncSession = Depends(get_db)) -> list[dict]:
    return await related_cases(db, case_id)


@app.get("/graph", dependencies=[Depends(require_role("reader"))])
async def graph_endpoint(db: AsyncSession = Depends(get_db)) -> dict:
    return await graph_snapshot(db)


def run() -> None:
    uvicorn.run("nexlexhub.api.main:app", host="0.0.0.0", port=8000, reload=False)
