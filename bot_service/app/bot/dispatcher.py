"""
Сборка Bot и Dispatcher.
"""
from aiogram import Bot, Dispatcher

from app.core.config import settings
from app.bot.handlers import router


def create_bot() -> Bot:
    """Создаёт бота."""
    return Bot(token=settings.telegram_bot_token)


def create_dispatcher() -> Dispatcher:
    """Создаёт диспетчер и подключает роутеры."""
    dp = Dispatcher()
    dp.include_router(router)
    return dp
