import pytest


@pytest.mark.asyncio
async def test_transaction_tag_create(cliente_autenticado):

    client, _ = cliente_autenticado

    payload = {
        "category": "Alimentação",
        "subcategory": "Café da Manhã",
        "type": "outcome",
    }

    response = await client.post("/api/v1/transaction-tags", json=payload)

    assert response.status_code == 201
