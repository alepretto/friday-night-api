from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from testcontainers.postgres import PostgresContainer

from app import domain
from app.api.deps.core import get_db, get_supabase_client
from app.main import app
from tests.factories import (
    AccountFactory,
    CurrencyFactory,
    FinancialInstitutionFactory,
    HoldingFactory,
    PaymentMethodFactory,
    TransactionFactory,
    TransactionTagFactory,
    UserFactory,
)


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

    async def _criar_usuario(**kwargs):
        novo_usuario = UserFactory().build(**kwargs)
        db_session.add(novo_usuario)
        await db_session.commit()
        await db_session.refresh(novo_usuario)
        return novo_usuario

    return _criar_usuario


@pytest_asyncio.fixture
async def cliente_autenticado(user_factory, db_session):

    usuario_test = await user_factory(is_active=True)

    mock_supabase = AsyncMock()

    mock_user_auth = AsyncMock()
    mock_user_auth.id = str(usuario_test.id)

    mock_supabase.auth.get_user.return_value = AsyncMock(user=mock_user_auth)

    # 3. Overrides
    # Forçamos o app a usar nossa db_session de teste e nosso mock do Supabase
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_supabase_client] = lambda: mock_supabase

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": "Bearer token_ficticio"},
    ) as client:
        yield client, usuario_test

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def financial_institutions_factory(db_session):

    async def _cria_financial_institution(**kwargs):

        model = FinancialInstitutionFactory().build(**kwargs)
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)
        return model

    return _cria_financial_institution


@pytest_asyncio.fixture
async def account_factory(db_session, user_factory, financial_institutions_factory):

    async def _cria_account(**kwargs):

        if "user_id" not in kwargs:
            user = await user_factory()
            kwargs["user_id"] = user.id

        if "financial_institution_id" not in kwargs:
            financial_institution = await financial_institutions_factory()
            kwargs["financial_institution_id"] = financial_institution.id

        model = AccountFactory.build(**kwargs)
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)

        return model

    return _cria_account


@pytest_asyncio.fixture
async def payment_method_factory(db_session, user_factory):

    async def _cria_payment(**kwargs):
        if "user_id" not in kwargs:
            user = await user_factory(is_active=True)
            kwargs["user_id"] = user.id

        model = PaymentMethodFactory.build(**kwargs)
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)
        return model

    return _cria_payment


@pytest_asyncio.fixture
async def currency_factory(db_session):

    async def _cria_currency(**kwargs):
        model = CurrencyFactory.build(**kwargs)
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)
        return model

    return _cria_currency


@pytest_asyncio.fixture
async def transaction_tag_factory(db_session, user_factory):

    async def _cria_tag(**kwargs):
        if "user_id" not in kwargs:
            user = await user_factory(is_active=True)
            kwargs["user_id"] = user.id

        model = TransactionTagFactory.build(**kwargs)
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)
        return model

    return _cria_tag


@pytest_asyncio.fixture
async def transaction_factory(
    db_session,
    user_factory,
    account_factory,
    transaction_tag_factory,
    currency_factory,
    payment_method_factory,
):

    async def _cria_transaction(**kwargs):

        if "user_id" not in kwargs:
            user = await user_factory()
            kwargs["user_id"] = user.id

        if "account_id" not in kwargs:
            account = await account_factory()
            kwargs["account_id"] = account.id

        if "transaction_tag_id" not in kwargs:
            tag = await transaction_tag_factory()
            kwargs["transaction_tag_id"] = tag.id

        if "currency_id" not in kwargs:
            currency = await currency_factory()
            kwargs["currency_id"] = currency.id

        if "payment_method_id" not in kwargs:
            method = await payment_method_factory()
            kwargs["payment_method_id"] = method.id

        transaction = TransactionFactory().build(**kwargs)
        db_session.add(transaction)
        await db_session.commit()
        await db_session.refresh(transaction)

        return transaction

    return _cria_transaction


@pytest_asyncio.fixture
async def holding_factory(db_session, user_factory, transaction_factory):

    async def _cria_holding(**kwargs):

        if "user_id" not in kwargs:
            user = await user_factory()
            kwargs["user_id"] = user.id

        if "transaction_id" not in kwargs:
            transaction = await transaction_factory()
            kwargs["transaction_id"] = transaction.id

        model = HoldingFactory.build(**kwargs)
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)
        return model

    return _cria_holding
