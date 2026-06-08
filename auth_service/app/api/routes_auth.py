"""
Эндпоинты Auth Service: регистрация, логин, профиль.
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_uc, get_current_user_id
from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError, InvalidTokenError, TokenExpiredError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    auth_uc: AuthUseCase = Depends(get_auth_uc),
):
    """Регистрация нового пользователя."""
    try:
        user_dict = await auth_uc.register(body.email, body.password)
        return UserPublic(**user_dict)
    except UserAlreadyExistsError as e:
        raise e


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    auth_uc: AuthUseCase = Depends(get_auth_uc),
):
    """Вход в систему. Возвращает JWT-токен."""
    try:
        token = await auth_uc.login(form.username, form.password)
        return TokenResponse(access_token=token)
    except InvalidCredentialsError as e:
        raise e


@router.get("/me", response_model=UserPublic)
async def me(
    user_id: int = Depends(get_current_user_id),
    auth_uc: AuthUseCase = Depends(get_auth_uc),
):
    """Профиль текущего пользователя."""
    try:
        user_dict = await auth_uc.me(user_id)
        return UserPublic(**user_dict)
    except UserNotFoundError as e:
        raise e
    except (InvalidTokenError, TokenExpiredError) as e:
        raise e
