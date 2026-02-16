import pytest


@pytest.mark.asyncio
async def test_user_updated_alterar_nome(cliente_autenticado):

    client, usuario = cliente_autenticado

    payload = {"first_name": "Nome Atualizado"}
    response = await client.patch("/api/v1/users/me", json=payload)

    assert response.status_code == 200
    assert response.json()["first_name"] == "Nome Atualizado"


@pytest.mark.asyncio
async def test_user_updated_varios_parametros(cliente_autenticado):

    client, usuario = cliente_autenticado

    payload = {"last_name": "pretto", "avatar_url": "kkjhkjh"}
    response = await client.patch("/api/v1/users/me", json=payload)

    assert response.status_code == 200
    assert response.json()["last_name"] == "pretto"
    assert response.json()["avatar_url"] == "kkjhkjh"


@pytest.mark.asyncio
async def test_user_delete_success(cliente_autenticado):

    client, usuario = cliente_autenticado

    response = await client.delete("/api/v1/users/me")

    assert response.status_code == 201
