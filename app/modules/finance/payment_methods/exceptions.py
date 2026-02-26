from http import HTTPStatus

from app.core.exception import FridayNightException


class PaymentMethodAlreadyExists(FridayNightException):
    def __init__(self, label: str, status_code: int = HTTPStatus.CONFLICT) -> None:

        message = f"Payment Method already exists: {label}"
        super().__init__(message, status_code)
