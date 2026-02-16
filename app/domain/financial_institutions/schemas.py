import uuid
from datetime import datetime
from typing import Optional

from sqlmodel.main import SQLModel

from .model import InstitutionType


class FinancialInstitutionsCreate(SQLModel):
    name: str
    type: InstitutionType
    icon_url: Optional[str] = None


class FinancialInstitutionsResponse(FinancialInstitutionsCreate):
    id: uuid.UUID
    created_at: datetime
