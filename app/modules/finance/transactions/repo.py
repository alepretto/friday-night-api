import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import case, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.modules.finance.categories.model import Category, CategoryType
from app.modules.finance.tags.model import Tag
from app.modules.finance.transactions.model import Transaction
from app.modules.finance.transactions.schemas import (
    CategorySummary,
    RecentTransactionResponse,
    TransactionSummaryResponse,
)


class TransactionRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: Transaction):
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)

        return model

    async def get_by_id(self, transaction_id: uuid.UUID) -> Optional[Transaction]:
        query = select(Transaction).where(Transaction.id == transaction_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, model: Transaction):
        await self.db.delete(model)
        await self.db.commit()

    async def list_by_account(
        self,
        account_id: uuid.UUID,
        user_id: uuid.UUID,
        date_start: Optional[datetime] = None,
        date_end: Optional[datetime] = None,
        params: Optional[Params] = None,
    ):
        query = (
            select(Transaction)
            .where(
                (Transaction.account_id == account_id)
                & (Transaction.user_id == user_id)
            )
            .order_by(Transaction.date_transaction.desc())  # type: ignore
        )

        if date_start:
            query = query.where(Transaction.date_transaction >= date_start)
        if date_end:
            query = query.where(Transaction.date_transaction <= date_end)

        return await apaginate(self.db, query, params=params)

    async def get_summary(
        self,
        user_id: uuid.UUID,
        date_start: datetime,
        date_end: datetime,
        account_id: Optional[uuid.UUID] = None,
    ) -> TransactionSummaryResponse:
        base_filter = (Transaction.user_id == user_id) & (
            Transaction.date_transaction >= date_start
        ) & (Transaction.date_transaction <= date_end)

        if account_id:
            base_filter = base_filter & (Transaction.account_id == account_id)

        # Query 1: totals
        totals_query = (
            select(
                sa_func.coalesce(
                    sa_func.sum(
                        case(
                            (Category.type == CategoryType.INCOME, Transaction.value),
                            else_=Decimal(0),
                        )
                    ),
                    Decimal(0),
                ).label("total_income"),
                sa_func.coalesce(
                    sa_func.sum(
                        case(
                            (Category.type == CategoryType.OUTCOME, Transaction.value),
                            else_=Decimal(0),
                        )
                    ),
                    Decimal(0),
                ).label("total_expense"),
                sa_func.count().label("transaction_count"),
            )
            .join(Tag, Transaction.tag_id == Tag.id)
            .join(Category, Tag.category_id == Category.id)
            .where(base_filter)
        )

        result = await self.db.execute(totals_query)
        row = result.one()
        total_income: Decimal = row.total_income
        total_expense: Decimal = row.total_expense
        transaction_count: int = row.transaction_count

        # Query 2: breakdown by category
        cat_query = (
            select(
                Category.label.label("category_label"),
                Category.type.label("category_type"),
                sa_func.sum(Transaction.value).label("total"),
                sa_func.count().label("transaction_count"),
            )
            .join(Tag, Transaction.tag_id == Tag.id)
            .join(Category, Tag.category_id == Category.id)
            .where(base_filter)
            .group_by(Category.id, Category.label, Category.type)
            .order_by(sa_func.sum(Transaction.value).desc())
        )

        cat_result = await self.db.execute(cat_query)
        by_category: list[CategorySummary] = []
        for cat_row in cat_result.all():
            cat_type_total = (
                total_income
                if cat_row.category_type == CategoryType.INCOME
                else total_expense
            )
            percent = (
                (cat_row.total / cat_type_total * 100)
                if cat_type_total > 0
                else Decimal(0)
            )
            by_category.append(
                CategorySummary(
                    category_label=cat_row.category_label,
                    category_type=cat_row.category_type.value,
                    total=cat_row.total,
                    transaction_count=cat_row.transaction_count,
                    percent=round(percent, 2),
                )
            )

        return TransactionSummaryResponse(
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense,
            transaction_count=transaction_count,
            by_category=by_category,
        )

    async def list_recent(
        self,
        user_id: uuid.UUID,
        limit: int = 10,
        account_id: Optional[uuid.UUID] = None,
    ) -> list[RecentTransactionResponse]:
        query = (
            select(Transaction)
            .options(
                joinedload(Transaction.tag).joinedload(Tag.category),  # type: ignore
                joinedload(Transaction.tag).joinedload(Tag.subcategory),  # type: ignore
            )
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.date_transaction.desc())  # type: ignore
            .limit(limit)
        )

        if account_id:
            query = query.where(Transaction.account_id == account_id)

        result = await self.db.execute(query)
        transactions = result.unique().scalars().all()

        return [
            RecentTransactionResponse(
                id=t.id,
                value=t.value,
                description=t.description,
                date_transaction=t.date_transaction,
                account_id=t.account_id,
                category_label=t.tag.category.label if t.tag and t.tag.category else "",
                category_type=(
                    t.tag.category.type.value if t.tag and t.tag.category else ""
                ),
                subcategory_label=(
                    t.tag.subcategory.label if t.tag and t.tag.subcategory else ""
                ),
            )
            for t in transactions
        ]
