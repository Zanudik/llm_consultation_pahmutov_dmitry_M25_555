"""
Подключение к Redis.
"""
import redis.asyncio as aioredis

from app.core.config import settings


async def get_redis() -> aioredis.Redis:
    """Возвращает клиент Redis."""
    return aioredis.from_url(settings.redis_url, decode_responses=True)
