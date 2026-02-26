from http import HTTPStatus

from app.core.exception import FridayNightException


class SubcategoryAlreadyExists(FridayNightException):
    def __init__(self, label: str, status_code: int = HTTPStatus.CONFLICT) -> None:
        message = f"Subcategory '{label}' already exists!"
        super().__init__(message, status_code)
