import uuid
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Optional
from uuid import UUID

from sqlalchemy import Column
from sqlmodel import TIMESTAMP, Field, SQLModel, UniqueConstraint, func


class AccountType(str, Enum):
    bank = auto()
    investment = auto()
    cash = auto()
    benefict = auto()


class AccountStatus(str, Enum):
    activate = auto()
    desactivate = auto()


class Account(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", sa_column_kwargs={"unique": False})
    financial_institution_id: UUID = Field(
        foreign_key="financial_institution.id", sa_column_kwargs={"unique": False}
    )
    status: AccountStatus
    type: AccountType
    subtype: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
    )

    class Config:
        table_args = (
            UniqueConstraint(
                "user_id",
                "financial_institution_id",
                "type",
                "subtype",
                name="unique_account",
            ),
        )
