import pytest


@pytest.mark.asyncio
async def test_transaction_tag_create_categories(cliente_autenticado):

    client, _ = cliente_autenticado

    payload = {
        "label": "Alimentação",
        "type": "outcome",
    }

    response = await client.post("/api/v1/categories", json=payload)
    assert response.status_code == 201

    response2 = await client.post("/api/v1/categories", json=payload)
    assert response2.status_code == 409
