"""
HTTP-исключения для Auth Service.
"""
from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """Базовая ошибка."""
    pass


class UserAlreadyExistsError(BaseHTTPException):
    """Email уже занят (409)."""
    def __init__(self, detail: str = "Пользователь с таким email уже существует"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidCredentialsError(BaseHTTPException):
    """Неверный email или пароль (401)."""
    def __init__(self, detail: str = "Неверный email или пароль"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class InvalidTokenError(BaseHTTPException):
    """Токен недействителен (401)."""
    def __init__(self, detail: str = "Недействительный токен"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class TokenExpiredError(BaseHTTPException):
    """Токен истёк (401)."""
    def __init__(self, detail: str = "Токен истёк"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UserNotFoundError(BaseHTTPException):
    """Пользователь не найден (404)."""
    def __init__(self, detail: str = "Пользователь не найден"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class PermissionDeniedError(BaseHTTPException):
    """Нет прав (403)."""
    def __init__(self, detail: str = "Недостаточно прав"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
