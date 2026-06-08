"""
Асинхронный движок и фабрика сессий для SQLite.
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

DATABASE_URL = f"sqlite+aiosqlite:///{settings.sqlite_path}"

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
