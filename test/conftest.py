import uuid
from datetime import datetime, timezone

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from testcontainers.postgres import PostgresContainer

from app import domain
from app.api.deps.core import get_current_user, get_db
from app.main import app


@pytest.fixture(scope="session")
def db_url():

    with PostgresContainer("postgres:15-alpine") as postgres:
        url = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        yield url


@pytest_asyncio.fixture(scope="function")
async def db_session(db_url):
    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def user_factory(db_session):

    async def _criar_usuario(
        id_=None,
        email="padrao@fridaynight.com",
        first_name="Usuário",
        last_name="Padrão",
        telegram_id=None,
        language="pt-br",
        created_at=None,
        is_premium=False,
        is_active=True,
        role="user",
    ):
        if id_ is None:
            id_ = uuid.uuid4()

        if created_at is None:
            created_at = datetime.now(tz=timezone.utc)

        novo_usuario = domain.User(
            id=id_,
            email=email,
            first_name=first_name,
            last_name=last_name,
            telegram_id=telegram_id,
            language=language,
            created_at=created_at,
            is_premium=is_premium,
            is_active=is_active,
            role=role,
        )
        db_session.add(novo_usuario)
        await db_session.commit()
        await db_session.refresh(novo_usuario)
        return novo_usuario

    return _criar_usuario


@pytest_asyncio.fixture
async def cliente_autenticado(user_factory, db_session):

    usuario_test = await user_factory()

    async def override_get_current_user():
        return usuario_test

    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client, usuario_test

    app.dependency_overrides.clear()
