import pytest


@pytest.mark.asyncio
async def test_holding_create(
    cliente_autenticado, transaction_factory, payment_method_factory
):

    client, user = cliente_autenticado

    payment_method = await payment_method_factory()
    transaction = await transaction_factory(
        user_id=user.id, payment_method_id=payment_method.id
    )

    payload = {
        "transaction_id": str(transaction.id),
        "user_id": str(user.id),
        "symbol": "BTC",
        "asset_type": "cripto",
        "quantity": 0.005,
        "price": 96555.09,
    }

    response = await client.post("/api/v1/holdings", json=payload)

    assert response.status_code == 201
