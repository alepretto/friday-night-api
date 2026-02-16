import pytest
from httpx import ASGITransport, AsyncClient

from app.api.deps.core import get_db
from app.main import app


@pytest.mark.asyncio
async def test_create_financial_institution(db_session):

    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        payload = {"name": "night-bank", "type": "bank"}
        response = await client.post("/api/v1/financial-institutions", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "night-bank"
    assert response.json()["type"] == "bank"
    assert "id" in response.json()

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_financial_institution_duplicate(db_session):

    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        payload = {"name": "night-bank", "type": "bank"}
        response = await client.post("/api/v1/financial-institutions", json=payload)

        assert response.status_code == 200

        response_2 = await client.post("/api/v1/financial-institutions", json=payload)

        assert response_2.status_code == 400
        assert (
            response_2.json()["message"]
            == "Resource already existis: night-bank - bank"
        )

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_financial_institution(db_session):

    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        payload = {"name": "night-bank", "type": "bank"}

        response_1 = await client.post("/api/v1/financial-institutions", json=payload)
        assert response_1.status_code == 200

        response_2 = await client.post("/api/v1/financial-institutions", json=payload)
        assert response_2.status_code == 400

        response = await client.get("/api/v1/financial-institutions")
        assert response.status_code == 200

    app.dependency_overrides.clear()
