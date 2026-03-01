import uuid

from app.core.exception import FridayNightException


class AccountNotFound(FridayNightException):
    def __init__(
        self,
        message: str = "Account Not Found",
        status_code: int = 404,
    ) -> None:
        super().__init__(message, status_code)


class AccountAlreadyExists(FridayNightException):
    def __init__(
        self,
        user_id: uuid.UUID,
        institution_id: uuid.UUID,
        type: str,
        subtype: str | None,
        status_code: int = 400,
    ) -> None:
        message = f"Resource already exists: {user_id} - {institution_id} - {type} - {subtype}"
        super().__init__(message, status_code)
