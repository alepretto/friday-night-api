import uuid

import pytest


BASE = "/api/v1/finance/currencies"


@pytest.mark.asyncio
async def test_create_currency(cliente_autenticado):
    client, _ = cliente_autenticado

    payload = {"label": "Real Brasileiro", "symbol": "BRL", "type": "fiat"}
    response = await client.post(BASE, json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["label"] == "Real Brasileiro"
    assert data["symbol"] == "BRL"
    assert data["type"] == "fiat"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_currency_duplicate(cliente_autenticado):
    client, _ = cliente_autenticado

    payload = {"label": "Real Brasileiro", "symbol": "BRL", "type": "fiat"}
    await client.post(BASE, json=payload)

    response = await client.post(BASE, json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_by_id(cliente_autenticado):
    client, _ = cliente_autenticado

    payload = {"label": "Bitcoin", "symbol": "BTC", "type": "cripto"}
    created = await client.post(BASE, json=payload)
    assert created.status_code == 201

    currency_id = created.json()["id"]
    response = await client.get(f"{BASE}/{currency_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == currency_id
    assert data["label"] == "Bitcoin"
    assert data["symbol"] == "BTC"


@pytest.mark.asyncio
async def test_get_by_id_not_found(cliente_autenticado):
    client, _ = cliente_autenticado

    response = await client.get(f"{BASE}/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_currencies(cliente_autenticado):
    client, _ = cliente_autenticado

    await client.post(BASE, json={"label": "Real Brasileiro", "symbol": "BRL", "type": "fiat"})
    await client.post(BASE, json={"label": "Dólar Americano", "symbol": "USD", "type": "fiat"})
    await client.post(BASE, json={"label": "Bitcoin", "symbol": "BTC", "type": "cripto"})

    response = await client.get(BASE)
    assert response.status_code == 200
    assert response.json()["total"] == 3


@pytest.mark.asyncio
async def test_list_filter_by_type(cliente_autenticado):
    client, _ = cliente_autenticado

    await client.post(BASE, json={"label": "Real Brasileiro", "symbol": "BRL", "type": "fiat"})
    await client.post(BASE, json={"label": "Dólar Americano", "symbol": "USD", "type": "fiat"})
    await client.post(BASE, json={"label": "Bitcoin", "symbol": "BTC", "type": "cripto"})

    response = await client.get(BASE, params={"type": "fiat"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert all(item["type"] == "fiat" for item in data["items"])

    response_cripto = await client.get(BASE, params={"type": "cripto"})
    assert response_cripto.json()["total"] == 1


@pytest.mark.asyncio
async def test_list_search_by_label(cliente_autenticado):
    client, _ = cliente_autenticado

    await client.post(BASE, json={"label": "Real Brasileiro", "symbol": "BRL", "type": "fiat"})
    await client.post(BASE, json={"label": "Real Argentino", "symbol": "ARS", "type": "fiat"})
    await client.post(BASE, json={"label": "Bitcoin", "symbol": "BTC", "type": "cripto"})

    response = await client.get(BASE, params={"label": "real"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert all("real" in item["label"].lower() for item in data["items"])


@pytest.mark.asyncio
async def test_list_search_by_symbol(cliente_autenticado):
    client, _ = cliente_autenticado

    await client.post(BASE, json={"label": "Real Brasileiro", "symbol": "BRL", "type": "fiat"})
    await client.post(BASE, json={"label": "Dólar Americano", "symbol": "USD", "type": "fiat"})
    await client.post(BASE, json={"label": "Bitcoin", "symbol": "BTC", "type": "cripto"})

    response = await client.get(BASE, params={"symbol": "b"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert all("b" in item["symbol"].lower() for item in data["items"])


@pytest.mark.asyncio
async def test_list_search_combined_filters(cliente_autenticado):
    client, _ = cliente_autenticado

    await client.post(BASE, json={"label": "Real Brasileiro", "symbol": "BRL", "type": "fiat"})
    await client.post(BASE, json={"label": "Real Argentino", "symbol": "ARS", "type": "fiat"})
    await client.post(BASE, json={"label": "Bitcoin", "symbol": "BTC", "type": "cripto"})

    response = await client.get(BASE, params={"label": "real", "type": "fiat"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2

    response = await client.get(BASE, params={"label": "real", "symbol": "BRL"})
    assert response.json()["total"] == 1


@pytest.mark.asyncio
async def test_list_empty(cliente_autenticado):
    client, _ = cliente_autenticado

    response = await client.get(BASE)
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["items"] == []
