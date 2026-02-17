from sqlmodel import SQLModel, Field
from uuid import UUID
from typing import Optional

class AccountType(str, enum.Enum):
    bank = "bank"
    investment = "investment"
    cash = "cash"
    benefict = "benefict"

class AccountStatus(str, enum.Enum):
    activate = "activate"
    desactivate = "desactivate"

class Account(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", sa_column_kwargs={"unique": False})
    financial_institution_id: UUID = Field(foreign_key="financial_institution.id", sa_column_kwargs={"unique": False})
    status: AccountStatus
    type: AccountType
    subtype: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    class Config:
        table_args = (
            UniqueConstraint("user_id", "financial_institution_id", "type", "subtype", name="unique_account"),
        )
