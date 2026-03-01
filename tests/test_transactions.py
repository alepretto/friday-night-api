from decimal import Decimal

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

    response = await client.post("/api/v1/finance/transactions", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["account_id"] == str(account.id)
    assert data["tag_id"] == str(tag.id)
    assert data["currency_id"] == str(currency.id)
    assert Decimal(data["value"]) == Decimal("100.0")


@pytest.mark.asyncio
async def test_transaction_create_with_description(
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
        "value": 50.0,
        "description": "Almoço no restaurante",
    }

    response = await client.post("/api/v1/finance/transactions", json=payload)

    assert response.status_code == 201
    assert response.json()["description"] == "Almoço no restaurante"


@pytest.mark.asyncio
async def test_transaction_list(
    cliente_autenticado,
    account_factory,
    transaction_factory,
):
    client, usuario = cliente_autenticado

    account = await account_factory(user_id=usuario.id)
    await transaction_factory(user_id=usuario.id, account_id=account.id)
    await transaction_factory(user_id=usuario.id, account_id=account.id)

    response = await client.get(f"/api/v1/finance/transactions?account_id={account.id}")

    assert response.status_code == 200
    assert response.json()["total"] == 2


@pytest.mark.asyncio
async def test_transaction_list_date_filter(
    cliente_autenticado,
    account_factory,
    transaction_factory,
):
    from datetime import datetime, timezone

    client, usuario = cliente_autenticado

    account = await account_factory(user_id=usuario.id)
    await transaction_factory(
        user_id=usuario.id,
        account_id=account.id,
        date_transaction=datetime(2024, 1, 15, tzinfo=timezone.utc),
    )
    await transaction_factory(
        user_id=usuario.id,
        account_id=account.id,
        date_transaction=datetime(2024, 3, 20, tzinfo=timezone.utc),
    )

    response = await client.get(
        f"/api/v1/finance/transactions?account_id={account.id}"
        "&date_start=2024-01-01T00:00:00&date_end=2024-02-01T00:00:00"
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1


@pytest.mark.asyncio
async def test_transaction_update(
    cliente_autenticado,
    account_factory,
    tag_factory,
    currency_factory,
    payment_method_factory,
    transaction_factory,
):
    client, usuario = cliente_autenticado

    account = await account_factory(user_id=usuario.id)
    tag = await tag_factory(user_id=usuario.id)
    payment_method = await payment_method_factory(user_id=usuario.id)
    currency = await currency_factory()
    transaction = await transaction_factory(
        user_id=usuario.id,
        account_id=account.id,
        tag_id=tag.id,
        payment_method_id=payment_method.id,
        currency_id=currency.id,
    )

    payload = {
        "account_id": str(account.id),
        "tag_id": str(tag.id),
        "payment_method_id": str(payment_method.id),
        "currency_id": str(currency.id),
        "value": 999.99,
        "description": "Atualizado",
    }

    response = await client.patch(
        f"/api/v1/finance/transactions/{transaction.id}", json=payload
    )

    assert response.status_code == 200
    assert Decimal(response.json()["value"]) == Decimal("999.99")
    assert response.json()["description"] == "Atualizado"


@pytest.mark.asyncio
async def test_transaction_update_not_found(
    cliente_autenticado,
    account_factory,
    tag_factory,
    currency_factory,
    payment_method_factory,
):
    import uuid

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
        "value": 50.0,
    }

    response = await client.patch(
        f"/api/v1/finance/transactions/{uuid.uuid4()}", json=payload
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_transaction_update_other_user(
    cliente_autenticado,
    user_factory,
    account_factory,
    tag_factory,
    currency_factory,
    payment_method_factory,
    transaction_factory,
):
    client, usuario = cliente_autenticado

    other_user = await user_factory()
    account = await account_factory(user_id=other_user.id)
    tag = await tag_factory(user_id=other_user.id)
    payment_method = await payment_method_factory(user_id=other_user.id)
    currency = await currency_factory()
    transaction = await transaction_factory(
        user_id=other_user.id,
        account_id=account.id,
        tag_id=tag.id,
        payment_method_id=payment_method.id,
        currency_id=currency.id,
    )

    payload = {
        "account_id": str(account.id),
        "tag_id": str(tag.id),
        "payment_method_id": str(payment_method.id),
        "currency_id": str(currency.id),
        "value": 50.0,
    }

    response = await client.patch(
        f"/api/v1/finance/transactions/{transaction.id}", json=payload
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_transaction_delete(
    cliente_autenticado,
    account_factory,
    transaction_factory,
):
    client, usuario = cliente_autenticado

    account = await account_factory(user_id=usuario.id)
    transaction = await transaction_factory(user_id=usuario.id, account_id=account.id)

    response = await client.delete(f"/api/v1/finance/transactions/{transaction.id}")
    assert response.status_code == 204

    list_response = await client.get(
        f"/api/v1/finance/transactions?account_id={account.id}"
    )
    assert list_response.json()["total"] == 0


@pytest.mark.asyncio
async def test_transaction_delete_not_found(cliente_autenticado):
    import uuid

    client, _ = cliente_autenticado

    response = await client.delete(f"/api/v1/finance/transactions/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_transaction_delete_other_user(
    cliente_autenticado,
    user_factory,
    account_factory,
    transaction_factory,
):
    client, _ = cliente_autenticado

    other_user = await user_factory()
    account = await account_factory(user_id=other_user.id)
    transaction = await transaction_factory(
        user_id=other_user.id, account_id=account.id
    )

    response = await client.delete(f"/api/v1/finance/transactions/{transaction.id}")
    assert response.status_code == 403
