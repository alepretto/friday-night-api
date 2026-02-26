from app.core.exception import FridayNightException


class FinancialInstitutionsAlreadyExists(FridayNightException):
    def __init__(self, institution: str, type: str, status_code: int = 400) -> None:
        message = f"Resource already exists: {institution} - {type}"
        super().__init__(message, status_code)
