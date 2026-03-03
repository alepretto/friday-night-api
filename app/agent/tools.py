import json
import uuid
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Any

from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.finance.accounts.model import Account, AccountStatus
from app.modules.finance.currencies.model import Currency
from app.modules.finance.currencies.repo import CurrencyRepo
from app.modules.finance.financial_institutions.model import FinancialInstitution
from app.modules.finance.payment_methods.repo import PaymentMethodRepo
from app.modules.finance.tags.repo import TagRepo
from app.modules.user.model import User
from app.agent.schema import PendingTransaction

TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "list_accounts",
            "description": "Lista as contas bancárias ativas do usuário.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tags",
            "description": "Lista as tags (categoria + subcategoria) ativas do usuário.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_payment_methods",
            "description": "Lista os métodos de pagamento ativos do usuário.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_currencies",
            "description": "Lista as moedas disponíveis (ex: BRL).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "propose_transaction",
            "description": (
                "Propõe uma transação para confirmação do usuário. "
                "Chame SEMPRE antes de registrar qualquer transação."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "UUID da conta"},
                    "tag_id": {"type": "string", "description": "UUID da tag"},
                    "payment_method_id": {
                        "type": "string",
                        "description": "UUID do método de pagamento",
                    },
                    "currency_id": {"type": "string", "description": "UUID da moeda"},
                    "value": {"type": "number", "description": "Valor da transação"},
                    "description": {"type": "string", "description": "Descrição opcional"},
                    "date": {
                        "type": "string",
                        "description": "Data ISO 8601 (ex: 2026-03-03T12:00:00). Padrão: hoje.",
                    },
                },
                "required": ["account_id", "tag_id", "payment_method_id", "currency_id", "value"],
            },
        },
    },
]


async def execute_tool(
    tool_name: str,
    tool_args: dict[str, Any],
    user: User,
    db: AsyncSession,
    chat_id: int,
    pending_store: dict[int, PendingTransaction],
) -> str:
    if tool_name == "list_accounts":
        return await _list_accounts(user, db)
    elif tool_name == "list_tags":
        return await _list_tags(user, db)
    elif tool_name == "list_payment_methods":
        return await _list_payment_methods(user, db)
    elif tool_name == "list_currencies":
        return await _list_currencies(db)
    elif tool_name == "propose_transaction":
        return await _propose_transaction(tool_args, user, db, chat_id, pending_store)
    else:
        return f"Tool desconhecida: {tool_name}"


async def _list_accounts(user: User, db: AsyncSession) -> str:
    query = (
        select(Account, FinancialInstitution)
        .join(FinancialInstitution, Account.financial_institution_id == FinancialInstitution.id)
        .where(
            (Account.user_id == user.id) & (Account.status == AccountStatus.activate)
        )
    )
    result = await db.execute(query)
    items = []
    for account, institution in result.all():
        label = f"{institution.name} - {account.type.value}"
        if account.subtype:
            label += f" ({account.subtype})"
        items.append({"id": str(account.id), "label": label})
    return json.dumps(items, ensure_ascii=False)


async def _list_tags(user: User, db: AsyncSession) -> str:
    page = await TagRepo(db).list_by_user(user.id, active=True, params=Params(1, 200))
    items = []
    for tag in page.items:
        cat = tag.category.label if tag.category else ""
        sub = tag.subcategory.label if tag.subcategory else ""
        items.append({
            "id": str(tag.id),
            "category": cat,
            "subcategory": sub,
            "label": f"{cat} / {sub}" if sub else cat,
        })
    return json.dumps(items, ensure_ascii=False)


async def _list_payment_methods(user: User, db: AsyncSession) -> str:
    page = await PaymentMethodRepo(db).list_by_user(
        user.id, params=Params(1, 200), active=True
    )
    items = [{"id": str(pm.id), "label": pm.label} for pm in page.items]
    return json.dumps(items, ensure_ascii=False)


async def _list_currencies(db: AsyncSession) -> str:
    page = await CurrencyRepo(db).list(symbol="BRL", params=Params(1, 10))
    items = [{"id": str(c.id), "symbol": c.symbol, "label": c.label} for c in page.items]
    return json.dumps(items, ensure_ascii=False)


async def _propose_transaction(
    args: dict[str, Any],
    user: User,
    db: AsyncSession,
    chat_id: int,
    pending_store: dict[int, PendingTransaction],
) -> str:
    account_id = uuid.UUID(args["account_id"])
    tag_id = uuid.UUID(args["tag_id"])
    payment_method_id = uuid.UUID(args["payment_method_id"])
    currency_id = uuid.UUID(args["currency_id"])
    value = Decimal(str(args["value"]))
    description: str | None = args.get("description")
    date_str: str | None = args.get("date")

    date: datetime | None = None
    if date_str:
        try:
            date = datetime.fromisoformat(date_str)
        except ValueError:
            date = None

    # Account label (join with institution)
    query = (
        select(Account, FinancialInstitution)
        .join(FinancialInstitution, Account.financial_institution_id == FinancialInstitution.id)
        .where(Account.id == account_id)
    )
    result = await db.execute(query)
    row = result.first()
    account_label = ""
    if row:
        account, institution = row
        account_label = f"{institution.name} - {account.type.value}"
        if account.subtype:
            account_label += f" ({account.subtype})"

    # Tag label
    tag = await TagRepo(db).get_by_id(tag_id, user.id)
    tag_label = ""
    if tag:
        cat = tag.category.label if tag.category else ""
        sub = tag.subcategory.label if tag.subcategory else ""
        tag_label = f"{cat} / {sub}" if sub else cat

    # Payment method label
    pm = await PaymentMethodRepo(db).get_by_id(payment_method_id, user.id)
    pm_label = pm.label if pm else str(payment_method_id)

    # Currency symbol
    currency = await db.get(Currency, currency_id)
    currency_symbol = currency.symbol if currency else "?"

    # Display date
    if date:
        display_date = date.strftime("%d/%m/%Y")
    else:
        today = datetime.now(timezone(timedelta(hours=-3)))
        display_date = today.strftime("%d/%m/%Y")

    pending_store[chat_id] = PendingTransaction(
        account_id=account_id,
        tag_id=tag_id,
        payment_method_id=payment_method_id,
        currency_id=currency_id,
        value=value,
        description=description,
        date=date,
        account_label=account_label,
        tag_label=tag_label,
        payment_method_label=pm_label,
        currency_symbol=currency_symbol,
    )

    desc_line = f"\n📝 {description}" if description else ""
    return (
        f"Vou registrar:\n"
        f"💰 {currency_symbol} {value:.2f}\n"
        f"📂 {tag_label}\n"
        f"🏦 {account_label}\n"
        f"💳 {pm_label}\n"
        f"📅 {display_date}"
        f"{desc_line}\n\n"
        f"Confirmar? (sim / não)"
    )
