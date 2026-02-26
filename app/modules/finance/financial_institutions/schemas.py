import uuid
from datetime import datetime
from typing import Optional

from sqlmodel.main import SQLModel

from .model import InstitutionType


class FinancialInstitutionCreate(SQLModel):
    name: str
    type: InstitutionType
    icon_url: Optional[str] = None


class FinancialInstitutionResponse(FinancialInstitutionCreate):
    id: uuid.UUID
    created_at: datetime
