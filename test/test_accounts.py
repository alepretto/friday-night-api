import pytest
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app.domain.accounts.model import Account, AccountStatus, AccountType
from app.domain.user.model import User
from app.domain.financial_institutions.model import FinancialInstitutions


@pytest.mark.asyncio
async def test_create_account_success(db_session):
    """
    Verifica que a criação de uma conta funciona e que os campos de timestamp são preenchidos.
    """
    # Cria usuário e instituição financeira necessários para a FK
    user = User(
        email="conta_teste@exemplo.com",
        first_name="Teste",
        last_name="Usuario",
        telegram_id=None,
        language="pt-br",
        is_premium=False,
        is_active=True,
    )
    institution = FinancialInstitutions(
        name="Banco Teste",
        type="bank",
        cnpj="00.000.000/0000-00",
    )
    db_session.add_all([user, institution])
    await db_session.commit()
    await db_session.refresh(user)
    await db_session.refresh(institution)

    # Cria a conta
    account = Account(
        user_id=user.id,
        financial_institution_id=institution.id,
        status=AccountStatus.activate,
        type=AccountType.bank,
        subtype=None,
    )
    db_session.add(account)
    await db_session.commit()
    await db_session.refresh(account)

    # Verificações
    assert isinstance(account.id, type(user.id))  # UUID
    assert account.user_id == user.id
    assert account.financial_institution_id == institution.id
    assert account.status == AccountStatus.activate
    assert account.type == AccountType.bank
    assert isinstance(account.created_at, datetime)
    assert account.created_at.tzinfo is not None  # timezone aware
    assert account.updated_at is None or isinstance(account.updated_at, datetime)


@pytest.mark.asyncio
async def test_create_account_duplicate_raises_integrity_error(db_session):
    """
    Verifica que a constraint única (user_id, financial_institution_id, type, subtype)
    impede a criação de contas duplicadas.
    """
    # Cria usuário e instituição financeira
    user = User(
        email="dup_teste@exemplo.com",
        first_name="Dup",
        last_name="Usuario",
        telegram_id=None,
        language="pt-br",
        is_premium=False,
        is_active=True,
    )
    institution = FinancialInstitutions(
        name="Banco Dup",
        type="bank",
        cnpj="11.111.111/1111-11",
    )
    db_session.add_all([user, institution])
    await db_session.commit()
    await db_session.refresh(user)
    await db_session.refresh(institution)

    # Primeira conta (deve ser criada com sucesso)
    account1 = Account(
        user_id=user.id,
        financial_institution_id=institution.id,
        status=AccountStatus.activate,
        type=AccountType.bank,
        subtype="corrente",
    )
    db_session.add(account1)
    await db_session.commit()
    await db_session.refresh(account1)

    # Segunda conta com os mesmos campos que violam a constraint única
    account2 = Account(
        user_id=user.id,
        financial_institution_id=institution.id,
        status=AccountStatus.activate,
        type=AccountType.bank,
        subtype="corrente",
    )
    db_session.add(account2)

    with pytest.raises(IntegrityError):
        await db_session.commit()
