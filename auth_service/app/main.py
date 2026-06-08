"""
Точка входа FastAPI для Auth Service.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes_auth import router as auth_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """При старте создаёт таблицы в БД."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    """Собирает приложение FastAPI."""
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(auth_router)

    @app.get("/health")
    async def health():
        """Проверка работоспособности."""
        return {"status": "ok", "env": settings.env}

    return app


app = create_app()
