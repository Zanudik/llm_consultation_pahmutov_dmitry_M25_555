"""
Модульные тесты: хеширование паролей и JWT.
"""
from app.core.security import hash_password, verify_password, create_access_token, decode_token


def test_hash_and_verify_password():
    """Хеш не равен паролю, verify работает."""
    password = "mysecret123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_create_and_decode_token():
    """Токен содержит sub, role, iat, exp и декодируется."""
    token = create_access_token(user_id=42, role="admin")
    payload = decode_token(token)

    assert payload["sub"] == "42"
    assert payload["role"] == "admin"
    assert "iat" in payload
    assert "exp" in payload
