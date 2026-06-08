"""
Зависимости FastAPI: сессии, репозитории, usecase, авторизация.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.usecases.auth import AuthUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncSession:
    """Создаёт сессию БД и закрывает после запроса."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_users_repo(session: AsyncSession = Depends(get_db)) -> UsersRepository:
    """Возвращает репозиторий пользователей."""
    return UsersRepository(session)


async def get_auth_uc(users_repo: UsersRepository = Depends(get_users_repo)) -> AuthUseCase:
    """Возвращает usecase авторизации."""
    return AuthUseCase(users_repo)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Извлекает user_id из JWT. Бросает ошибку, если токен невалидный."""
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        return user_id
    except ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTError:
        raise InvalidTokenError()
