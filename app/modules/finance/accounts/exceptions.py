import uuid

from app.core.exception import FridayNightException


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
