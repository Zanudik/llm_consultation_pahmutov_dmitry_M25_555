"""
Хеширование паролей и работа с JWT.
"""
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Возвращает хеш пароля (bcrypt)."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, совпадает ли пароль с хешем."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, role: str) -> str:
    """Создаёт JWT с полями sub, role, iat, exp."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)
    return token


def decode_token(token: str) -> dict:
    """Раскодирует и проверяет JWT. Возвращает payload."""
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    return payload
