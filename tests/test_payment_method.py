import pytest


@pytest.mark.asyncio
async def test_payment_method_create(cliente_autenticado):

    client, _ = cliente_autenticado

    payload = {
        "label": "Cartão de Crédito",
    }

    response = await client.post("/api/v1/finance/payment-methods", json=payload)
    assert response.status_code == 201

    response2 = await client.post("/api/v1/finance/payment-methods", json=payload)
    assert response2.status_code == 409
