import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import TIMESTAMP, Column, Index, func, text
from sqlmodel import Field, SQLModel


class AccountType(str, Enum):
    bank = "bank"
    investment = "investment"
    cash = "cash"
    benefit = "benefit"  # corrigido


class AccountStatus(str, Enum):
    activate = "activate"
    deactivate = "deactivate"


class Account(SQLModel, table=True):
    __tablename__ = "accounts"  # type: ignore
    __table_args__ = (
        Index(
            "unique_account_with_subtype",
            "user_id",
            "financial_institution_id",
            "type",
            "subtype",
            unique=True,
            postgresql_where=text("subtype IS NOT NULL"),
        ),
        # Índice para quando subtype é NULL
        Index(
            "unique_account_null_subtype",
            "user_id",
            "financial_institution_id",
            "type",
            unique=True,
            postgresql_where=text("subtype IS NULL"),
        ),
    )

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", sa_column_kwargs={"unique": False})
    financial_institution_id: UUID = Field(
        foreign_key="financial_institutions.id", sa_column_kwargs={"unique": False}
    )
    status: AccountStatus
    type: AccountType
    subtype: Optional[str] = None

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=True,
        ),
    )
