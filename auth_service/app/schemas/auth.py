"""
Pydantic-схемы для регистрации и токенов.
"""
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    """Тело запроса на регистрацию."""
    email: str = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=6, description="Пароль, минимум 6 символов")


class TokenResponse(BaseModel):
    """Ответ с JWT-токеном."""
    access_token: str = Field(..., description="JWT-токен")
    token_type: str = Field(default="bearer", description="Тип токена")
