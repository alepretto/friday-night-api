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

    method_id = response.json()["id"]

    response_get = await client.get(f"/api/v1/finance/payment-methods/{method_id}")
    assert response_get.status_code == 200

    response_list = await client.get("/api/v1/finance/payment-methods")
    assert response_list.status_code == 200

    assert response_list.json()["total"] == 1


@pytest.mark.asyncio
async def test_toogle_status(cliente_autenticado):

    client, _ = cliente_autenticado

    payload = {"label": "Cartão de Crédito", "active": True}

    response = await client.post("/api/v1/finance/payment-methods", json=payload)
    assert response.status_code == 201

    method_id = response.json()["id"]

    resp_deacativate = await client.patch(
        f"/api/v1/finance/payment-methods/{method_id}/deactivate"
    )
    assert resp_deacativate.status_code == 200

    response_get = await client.get(f"/api/v1/finance/payment-methods/{method_id}")
    assert not response_get.json()["active"]

    resp_acativate = await client.patch(
        f"/api/v1/finance/payment-methods/{method_id}/activate"
    )
    assert resp_acativate.status_code == 200

    response_get = await client.get(f"/api/v1/finance/payment-methods/{method_id}")
    assert response_get.json()["active"]
