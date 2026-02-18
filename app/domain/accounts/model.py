from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import TIMESTAMP, Column, Index, func, text
from sqlmodel import Field, Relationship, SQLModel
from uuid6 import uuid7

if TYPE_CHECKING:
    from app.domain.user.model import User


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

    id: UUID = Field(
        primary_key=True, index=True, nullable=False, default_factory=uuid7
    )
    user_id: UUID = Field(
        foreign_key="users.id", sa_column_kwargs={"unique": False}, ondelete="CASCADE"
    )
    financial_institution_id: UUID = Field(
        foreign_key="financial_institutions.id",
        sa_column_kwargs={"unique": False},
        index=True,
    )
    status: AccountStatus
    type: AccountType
    subtype: Optional[str] = None

    created_at: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
        ),
    )
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )

    user: "User" = Relationship(back_populates="accounts")
