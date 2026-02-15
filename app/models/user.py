import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import TIMESTAMP, String
from sqlmodel import BigInteger, Field, SQLModel, func


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: uuid.UUID = Field(primary_key=True, index=True, nullable=False)
    telegram_id: Optional[int] = Field(
        sa_column=Column(BigInteger, nullable=True, index=True, unique=True)
    )

    email: str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    username: Optional[str] = Field(default=None)
    avatar_url: Optional[str] = Field(default=None)
    language: str = Field(
        sa_column=Column(String(), server_default="pt-br", nullable=False)
    )

    is_premium: bool = Field(default=False)
    is_active: bool = Field(default=True)
    role: str = Field(default="user")
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now())
    )
