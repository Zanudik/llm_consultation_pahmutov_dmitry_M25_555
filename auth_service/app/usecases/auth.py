"""
Бизнес-логика регистрации, логина и профиля.
"""
from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.users import UsersRepository


class AuthUseCase:
    """Сценарии работы с пользователями."""

    def __init__(self, users_repo: UsersRepository):
        self._users_repo = users_repo

    async def register(self, email: str, password: str) -> dict:
        """Регистрирует пользователя. Возвращает словарь с id, email, role, created_at."""
        existing = await self._users_repo.get_by_email(email)
        if existing is not None:
            raise UserAlreadyExistsError()

        hashed = hash_password(password)
        user = await self._users_repo.create(email, hashed)

        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
        }

    async def login(self, email: str, password: str) -> str:
        """Проверяет пароль и возвращает JWT-токен."""
        user = await self._users_repo.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        token = create_access_token(user.id, user.role)
        return token

    async def me(self, user_id: int) -> dict:
        """Возвращает профиль пользователя по id."""
        user = await self._users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
        }
