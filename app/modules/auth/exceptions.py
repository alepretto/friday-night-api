from app.core.exception import FridayNightException


class SessionFiledError(FridayNightException):
    def __init__(
        self,
        message: str = "Não foi possível iniciar a Sessão.",
        status_code: int = 401,
    ) -> None:
        super().__init__(message, status_code)


class AuthUserNotFound(FridayNightException):
    def __init__(
        self,
        message: str = "O usuário náo foi encontrado na autenticação.",
        status_code: int = 401,
    ) -> None:
        super().__init__(message, status_code)
