import pytest


@pytest.mark.asyncio
async def test_transaction_tag_create_categories(cliente_autenticado):

    client, _ = cliente_autenticado

    payload = {
        "label": "Alimentação",
        "type": "outcome",
    }

    response = await client.post("/api/v1/finance/categories", json=payload)
    assert response.status_code == 201

    response2 = await client.post("/api/v1/finance/categories", json=payload)
    assert response2.status_code == 409

    responseGet = await client.get(
        f"/api/v1/finance/categories/{response.json()['id']}"
    )
    assert responseGet.status_code == 200


@pytest.mark.asyncio
async def test_transaction_tag_create_subcategory(
    cliente_autenticado, category_factory
):

    client, user = cliente_autenticado

    category = await category_factory()

    payload = {
        "user_id": str(user.id),
        "category_id": str(category.id),
        "label": "Cafezinho",
    }

    response = await client.post("/api/v1/finance/subcategories", json=payload)
    assert response.status_code == 201

    response2 = await client.post("/api/v1/finance/subcategories", json=payload)
    assert response2.status_code == 409

    response_get = await client.get(
        f"/apip/v1/finance/subcategories/{response.json()['id']}"
    )
    assert response_get.status_code == 200


@pytest.mark.asyncio
async def test_transaction_tag_create(
    cliente_autenticado, category_factory, subcategory_factory
):
    client, user = cliente_autenticado

    category = await category_factory()
    subcategory = await subcategory_factory()

    payload = {
        "user_id": str(user.id),
        "category_id": str(category.id),
        "subcategory_id": str(subcategory.id),
        "active": True,
    }

    response = await client.post("/api/v1/finance/tags", json=payload)
    assert response.status_code == 201

    response2 = await client.post("/api/v1/finance/tags", json=payload)
    assert response2.status_code == 409

    response_get = await client.get(f"/api/v1/finance/tags/{response.json()['id']}")
    assert response_get.status_code == 200
