"""
Точка входа FastAPI для Bot Service.
"""
from fastapi import FastAPI

from app.core.config import settings


def create_app() -> FastAPI:
    """Собирает приложение FastAPI."""
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )

    @app.get("/health")
    async def health():
        """Проверка работоспособности."""
        return {"status": "ok", "env": settings.env}

    return app


app = create_app()
