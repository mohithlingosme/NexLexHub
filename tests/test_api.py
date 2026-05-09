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
        response = await client.post(
            "/search",
            json={"query": "execution"},
            headers={"X-API-Key": "dev-api-key"},
        )
        assert response.status_code == 200
        assert response.json()
