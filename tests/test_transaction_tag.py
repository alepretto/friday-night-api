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

    category = await category_factory(user_id=user.id)
    category_id = str(category.id)
    payload = {
        "user_id": str(user.id),
        "category_id": category_id,
        "label": "Cafezinho",
    }

    response = await client.post("/api/v1/finance/subcategories", json=payload)
    assert response.status_code == 201

    response2 = await client.post("/api/v1/finance/subcategories", json=payload)
    assert response2.status_code == 409

    response_get = await client.get(
        f"/api/v1/finance/subcategories/{response.json()['id']}"
    )
    assert response_get.status_code == 200

    payload2 = {
        "user_id": str(user.id),
        "category_id": category_id,
        "label": "Mercadinho",
    }

    response = await client.post("/api/v1/finance/subcategories", json=payload2)
    assert response.status_code == 201

    response = await client.get(f"/api/v1/finance/subcategories/list/{category_id}")
    assert response.status_code == 200
    assert response.json()["total"] == 2


@pytest.mark.asyncio
async def test_transaction_tag_create(
    cliente_autenticado, category_factory, subcategory_factory
):
    client, user = cliente_autenticado

    category = await category_factory(user_id=user.id)
    subcategory = await subcategory_factory(category_id=category.id)

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


@pytest.mark.asyncio
async def test_create_multiple_tags(
    cliente_autenticado, category_factory, subcategory_factory
):

    client, user = cliente_autenticado

    category = await category_factory(user_id=user.id)

    subcat1 = await subcategory_factory(user_id=user.id, category_id=category.id)
    subcat2 = await subcategory_factory(user_id=user.id, category_id=category.id)

    payload = {
        "user_id": str(user.id),
        "category_id": str(category.id),
        "subcategory_id": str(subcat1.id),
        "active": True,
    }
    response1 = await client.post("/api/v1/finance/tags", json=payload)
    assert response1.status_code == 201

    payload2 = {
        "user_id": str(user.id),
        "category_id": str(category.id),
        "subcategory_id": str(subcat2.id),
        "active": False,
    }

    response2 = await client.post("/api/v1/finance/tags", json=payload2)
    assert response2.status_code == 201

    response_list = await client.get("/api/v1/finance/tags?active=true")

    assert response_list.status_code == 200
    assert response_list.json()["total"] == 1


@pytest.mark.asyncio
async def test_transaction_tag_toggle(
    cliente_autenticado, category_factory, subcategory_factory
):
    client, user = cliente_autenticado

    category = await category_factory(user_id=user.id)
    subcategory = await subcategory_factory(category_id=category.id)

    payload = {
        "user_id": str(user.id),
        "category_id": str(category.id),
        "subcategory_id": str(subcategory.id),
        "active": True,
    }

    response = await client.post("/api/v1/finance/tags", json=payload)
    assert response.status_code == 201

    tag_id = response.json()["id"]

    r_deactive = await client.patch(f"/api/v1/finance/tags/{tag_id}/deactivate")
    assert r_deactive.status_code == 200

    response = await client.get(f"/api/v1/finance/tags/{tag_id}")
    assert response.status_code == 200
    assert not response.json()["active"]

    r_active = await client.patch(f"/api/v1/finance/tags/{tag_id}/activate")
    assert r_active.status_code == 200

    response = await client.get(f"/api/v1/finance/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["active"]
