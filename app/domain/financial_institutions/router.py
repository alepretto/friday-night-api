from fastapi import APIRouter, Depends

from app.api.deps.domain import get_financial_institution_service
from app.domain.financial_institutions.schemas import (
    FinancialInstitutionsCreate,
    FinancialInstitutionsResponse,
)
from app.domain.financial_institutions.service import FinancialInstitutionService

router = APIRouter(prefix="/financial-institutions")


@router.post("", response_model=FinancialInstitutionsResponse)
async def create_financial_institution(
    infos_data: FinancialInstitutionsCreate,
    service: FinancialInstitutionService = Depends(get_financial_institution_service),
):

    return await service.create_update(infos_data)
