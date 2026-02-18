import pytest


@pytest.mark.asyncio
async def test_create_currency(cliente_autenticado):

    payload = {"label": "Real", "symbol": "R$", "type": "fiat"}

    client, _ = cliente_autenticado

    response = await client.post("/api/v1/currencies", json=payload)

    assert response.status_code == 201
