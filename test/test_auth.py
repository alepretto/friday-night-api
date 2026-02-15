from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.api.deps.core import get_auth_service
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_auth_service():
    mock_service = AsyncMock()

    async def override_get_auth_service():
        return mock_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service

    yield mock_service

    app.dependency_overrides.clear()


def test_signup_endpoint_success(mock_auth_service):

    mock_auth_service.register_new_user.return_value = {
        "id": "550e8400-e29b-41d4-a716-446655440000",  # Seu padrão UUID
        "email": "ale@fridaynight.com",
        "first_name": "Ale",
        "last_name": "Pretto",
    }

    payload = {
        "email": "ale@fridaynight.com",
        "password": "senha-super-forte",
        "first_name": "Ale",
        "last_name": "Pretto",
    }

    response = client.post("/api/v1/auth/signup", json=payload)

    assert response.status_code == 200
    assert (
        response.json()["message"] == "Usuário criado. Verifique o e-mail se necessário"
    )
    assert response.json()["user"]["email"] == "ale@fridaynight.com"

    mock_auth_service.register_new_user.assert_called_once()
