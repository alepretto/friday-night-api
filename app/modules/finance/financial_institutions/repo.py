import uuid

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.finance.financial_institutions.model import (
    FinancialInstitution,
    InstitutionType,
)

from .exceptions import FinancialInstitutionNotFound, FinancialInstitutionsAlreadyExists


class FinancialInstitutionsRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: FinancialInstitution):

        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return model

        except IntegrityError:
            await self.db.rollback()

            raise FinancialInstitutionsAlreadyExists(
                institution=model.name, type=model.type.value
            ) from None

    async def get_by_id(self, institution_id: uuid.UUID) -> FinancialInstitution:
        query = select(FinancialInstitution).where(
            FinancialInstitution.id == institution_id
        )
        model = await self.db.scalar(query)
        if not model:
            raise FinancialInstitutionNotFound()
        return model

    async def list(
        self, type: InstitutionType | None = None, params: Params | None = None
    ):

        query = select(FinancialInstitution)
        if type is not None:
            query = query.where(FinancialInstitution.type == type)

        query = query.order_by(FinancialInstitution.name, FinancialInstitution.type)

        return await apaginate(self.db, query, params=params)
