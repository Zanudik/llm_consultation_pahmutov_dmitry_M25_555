"""
Настройки Bot Service через переменные окружения.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Все настройки приложения, читаются из .env."""
    app_name: str
    env: str = "local"

    telegram_bot_token: str

    jwt_secret: str
    jwt_alg: str = "HS256"

    redis_url: str = "redis://redis:6379/0"
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672//"

    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "inclusionai/ling-2.6-1t:free"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "bot-service"

    class Config:
        env_file = ".env"


settings = Settings()
