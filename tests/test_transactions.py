import pytest


@pytest.mark.asyncio
async def test_transaction_create(
    cliente_autenticado,
    account_factory,
    tag_factory,
    currency_factory,
    payment_method_factory,
):

    client, usuario = cliente_autenticado

    account = await account_factory(user_id=usuario.id)
    tag = await tag_factory(user_id=usuario.id)
    payment_method = await payment_method_factory(user_id=usuario.id)
    currency = await currency_factory()

    payload = {
        "account_id": str(account.id),
        "tag_id": str(tag.id),
        "payment_method_id": str(payment_method.id),
        "currency_id": str(currency.id),
        "value": 100.0,
        "date_transaction": "2020-03-01 10:15",
    }

    response = await client.post("/api/v1/transactions", json=payload)

    assert response.status_code == 201
