import uuid

from fastapi_pagination import Params

from app.modules.finance.payment_methods.model import PaymentMethod
from app.modules.finance.payment_methods.repo import PaymentMethodRepo
from app.modules.finance.payment_methods.schemas import PaymentMethodCreate
from app.modules.user.model import User


class PaymentMethodService:
    def __init__(self, repo: PaymentMethodRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: PaymentMethodCreate, user: User):
        model = PaymentMethod.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_updated(model)

    async def get_by_id(self, payment_method_id: uuid.UUID, user: User):

        return await self.repo.get_by_id(payment_method_id, user.id)

    async def list_by_user(
        self, user: User, is_active: bool | None = None, params: Params | None = None
    ):

        return await self.repo.list_by_user(user.id, params=params, active=is_active)
