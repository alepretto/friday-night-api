from http import HTTPStatus

from app.core.exception import FridayNightException
from app.domain.transaction_tags.model import TransactionTagType


class TagAlreadExists(FridayNightException):
    def __init__(
        self,
        category: str,
        subcategory: str,
        type: TransactionTagType,
        status_code: int = HTTPStatus.CONFLICT,
    ) -> None:

        message = f"Tag Already Exists! {category} - {subcategory} - {type}"
        super().__init__(message, status_code)
