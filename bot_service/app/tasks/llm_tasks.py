"""
Celery-задача: запрос к LLM и отправка ответа пользователю.
"""
from aiogram import Bot

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterClient


@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str):
    """
    Отправляет запрос к OpenRouter и пересылает ответ в Telegram.
    Выполняется асинхронно через Celery worker.
    """
    import asyncio

    async def _run():
        client = OpenRouterClient()
        answer = await client.ask(prompt)

        bot = Bot(token=settings.telegram_bot_token)
        await bot.send_message(tg_chat_id, answer)
        await bot.session.close()

    asyncio.run(_run())
