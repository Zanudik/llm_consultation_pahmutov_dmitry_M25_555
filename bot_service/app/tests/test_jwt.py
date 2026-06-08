"""
Модульные тесты: проверка JWT.
"""
import pytest
from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def test_decode_valid_token():
    """Валидный токен декодируется и возвращает payload."""
    token = jwt.encode(
        {"sub": "99", "role": "user", "exp": 9999999999},
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )
    payload = decode_and_validate(token)
    assert payload["sub"] == "99"
    assert payload["role"] == "user"


def test_decode_invalid_token():
    """Мусорная строка вызывает ошибку."""
    with pytest.raises(Exception):
        decode_and_validate("not.a.token")
