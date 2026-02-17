import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

from app.domain.accounts.model import AccountStatus, AccountType


class AccountCreate(SQLModel):
    financial_institution_id: uuid.UUID
    status: AccountStatus
    type: AccountType
    subtype: Optional[str] = None


class AccountResponse(AccountCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
