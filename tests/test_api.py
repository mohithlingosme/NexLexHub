from httpx import ASGITransport, AsyncClient
import pytest

from nexlexhub.api.main import app
from nexlexhub.db.session import SessionLocal
from nexlexhub.services.bootstrap import seed_demo_data


@pytest.mark.asyncio
async def test_health_and_search() -> None:
    async with SessionLocal() as session:
        await seed_demo_data(session)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        health = await client.get("/health")
        assert health.status_code == 200
        token_response = await client.post(
            "/auth/login",
            json={"email": "analyst@nexlexhub.local", "password": "analyst123"},
        )
        assert token_response.status_code == 200
        token = token_response.json()["access_token"]
        response = await client.post(
            "/search",
            json={"query": "execution"},
            headers={"X-API-Key": "dev-api-key"},
        )
        assert response.status_code == 200
        assert response.json()
        analysis = await client.post(
            "/legal-analysis",
            json={"query": "execution"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert analysis.status_code == 200
        statutes = await client.get("/statutes", headers={"X-API-Key": "dev-api-key"})
        assert statutes.status_code == 200
        alerts = await client.get("/alerts", headers={"X-API-Key": "dev-api-key"})
        assert alerts.status_code == 200
