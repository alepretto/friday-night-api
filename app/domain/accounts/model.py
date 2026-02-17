import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, TIMESTAMP, UniqueConstraint, func
from sqlmodel import Field, SQLModel


class AccountType(str, Enum):
    bank = "bank"
    investment = "investment"
    cash = "cash"
    benefit = "benefit"  # corrigido


class AccountStatus(str, Enum):
    activate = "activate"
    deactivate = "deactivate"  # corrigido


class Account(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", sa_column_kwargs={"unique": False})
    financial_institution_id: UUID = Field(
        foreign_key="financial_institution.id", sa_column_kwargs={"unique": False}
    )
    status: AccountStatus
    type: AccountType
    subtype: Optional[str] = None

    # Usa server_default para que o banco preencha o timestamp
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
        )
    )
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=True,
        ),
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "financial_institution_id",
            "type",
            "subtype",
            name="unique_account",
        ),
    )
