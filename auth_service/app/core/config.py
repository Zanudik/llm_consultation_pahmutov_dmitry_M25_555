"""
Настройки Auth Service через переменные окружения.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Все настройки приложения, читаются из .env."""
    app_name: str
    env: str = "local"

    jwt_secret: str
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    sqlite_path: str = "./auth.db"

    class Config:
        env_file = ".env"


settings = Settings()
