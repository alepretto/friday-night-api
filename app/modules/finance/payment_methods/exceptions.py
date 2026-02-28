from http import HTTPStatus

from app.core.exception import FridayNightException


class PaymentMethodAlreadyExists(FridayNightException):
    def __init__(self, label: str, status_code: int = HTTPStatus.CONFLICT) -> None:

        message = f"Payment Method already exists: {label}"
        super().__init__(message, status_code)


class PaymentMethodNotFound(FridayNightException):
    def __init__(
        self,
        message: str = "Payment Method Not Found",
        status_code: int = HTTPStatus.NOT_FOUND,
    ) -> None:
        super().__init__(message, status_code)


class PaymentMethodAlreadyActivate(FridayNightException):
    def __init__(
        self,
        message: str = "Payment Method already activate",
        status_code: int = HTTPStatus.BAD_REQUEST,
    ) -> None:
        super().__init__(message, status_code)


class PaymentMethodAlreadyDeactivate(FridayNightException):
    def __init__(
        self,
        message: str = "Payment Method already deactivate",
        status_code: int = HTTPStatus.BAD_REQUEST,
    ) -> None:
        super().__init__(message, status_code)
