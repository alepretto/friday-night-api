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


class TelegramAuthError(FridayNightException):
    def __init__(
        self,
        message: str = "Autenticação Telegram inválida.",
        status_code: int = 401,
    ) -> None:
        super().__init__(message, status_code)


class TelegramUserNotLinked(FridayNightException):
    def __init__(
        self,
        message: str = "Nenhum usuário vinculado a este Telegram.",
        status_code: int = 404,
    ) -> None:
        super().__init__(message, status_code)
