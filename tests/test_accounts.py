import pytest


@pytest.mark.asyncio
async def test_create_account_success(
    cliente_autenticado, financial_institutions_factory
):
    """
    Verifica que a criação de uma conta funciona e que os campos de timestamp são preenchidos.
    """

    institution = await financial_institutions_factory()

    client, _ = cliente_autenticado

    payload = {
        "financial_institution_id": str(institution.id),
        "status": "activate",
        "type": "bank",
    }
    response = await client.post("/api/v1/accounts", json=payload)

    assert response.status_code == 201
    assert response.json()["financial_institution_id"] == str(institution.id)


@pytest.mark.asyncio
async def test_create_account_error(
    cliente_autenticado, financial_institutions_factory
):
    """
    Verifica que a criação de uma conta funciona e que os campos de timestamp são preenchidos.
    """

    institution = await financial_institutions_factory()

    client, _ = cliente_autenticado
    payload = {
        "financial_institution_id": str(institution.id),
        "status": "activate",
        "type": "bank",
    }
    response = await client.post("/api/v1/accounts", json=payload)
    assert response.status_code == 201

    response_2 = await client.post("/api/v1/accounts", json=payload)
    assert response_2.status_code == 400


@pytest.mark.asyncio
async def test_listagem_account(cliente_autenticado, account_factory):

    client, user = cliente_autenticado

    _ = await account_factory(user_id=user.id)
    _ = await account_factory(user_id=user.id)

    response = await client.get("/api/v1/accounts")

    assert response.status_code == 200
    assert response.json()["total"] == 2
