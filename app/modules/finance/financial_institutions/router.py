import uuid

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.api.deps.finance import get_financial_institution_service
from app.modules.finance.financial_institutions.model import InstitutionType
from app.modules.finance.financial_institutions.schemas import (
    FinancialInstitutionCreate,
    FinancialInstitutionResponse,
)
from app.modules.finance.financial_institutions.service import (
    FinancialInstitutionService,
)

router = APIRouter(prefix="/financial-institutions")


@router.post("", response_model=FinancialInstitutionResponse)
async def create_financial_institution(
    infos_data: FinancialInstitutionCreate,
    service: FinancialInstitutionService = Depends(get_financial_institution_service),
):

    return await service.create_update(infos_data)


@router.get("/{institution_id}", response_model=FinancialInstitutionResponse)
async def get_financial_institution(
    institution_id: uuid.UUID,
    service: FinancialInstitutionService = Depends(get_financial_institution_service),
):
    return await service.get_by_id(institution_id)


@router.get("", response_model=Page[FinancialInstitutionResponse])
async def list_financial_institution(
    type: InstitutionType | None = None,
    service: FinancialInstitutionService = Depends(get_financial_institution_service),
):

    return await service.list(type=type)
