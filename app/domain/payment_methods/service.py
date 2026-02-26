from app.domain.payment_methods.model import PaymentMethod
from app.domain.payment_methods.repo import PaymentMethodRepo
from app.domain.payment_methods.schemas import PaymentMethodCreate
from app.modules.user.model import User


class PaymentMethodService:
    def __init__(self, repo: PaymentMethodRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: PaymentMethodCreate, user: User):
        model = PaymentMethod.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_updated(model)
