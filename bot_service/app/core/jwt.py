"""
Проверка JWT-токена (только валидация, без создания).
"""
from jose import jwt

from app.core.config import settings


def decode_and_validate(token: str) -> dict:
    """
    Проверяет подпись и срок действия токена.
    Возвращает payload, если токен валидный.
    Бросает ошибку, если токен неверный или истёк.
    """
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    return payload
