"""
Мок-тесты: обработчики Telegram с fakeredis.
"""
import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, User, Chat

from app.bot.handlers import cmd_token, handle_message


@pytest.fixture
def fake_message():
    """Создаёт фейковое сообщение."""
    msg = AsyncMock(spec=Message)
    msg.from_user = User(id=12345, is_bot=False, first_name="Test")
    msg.chat = Chat(id=12345, type="private")
    msg.answer = AsyncMock()
    return msg


@pytest.mark.asyncio
async def test_token_command_saves_to_redis(fake_message):
    """Команда /token сохраняет токен в Redis."""
    from app.core.config import settings
    from jose import jwt

    token = jwt.encode(
        {"sub": "1", "role": "user", "exp": 9999999999},
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )
    fake_message.text = f"/token {token}"

    with patch("app.bot.handlers.get_redis") as mock_redis:
        mock_redis_instance = AsyncMock()
        mock_redis.return_value = mock_redis_instance
        await cmd_token(fake_message)

        # Проверяем, что токен сохранён в Redis
        mock_redis_instance.set.assert_called_once_with("token:12345", token)
        fake_message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_message_without_token(fake_message):
    """Без токена бот просит авторизоваться."""
    fake_message.text = "Привет"

    with patch("app.bot.handlers.get_redis") as mock_redis:
        mock_redis_instance = AsyncMock()
        mock_redis_instance.get.return_value = None
        mock_redis.return_value = mock_redis_instance

        await handle_message(fake_message)

        fake_message.answer.assert_called_once()
        assert "токен" in fake_message.answer.call_args[0][0].lower()


@pytest.mark.asyncio
async def test_message_with_token_calls_celery(fake_message):
    """С токеном сообщение отправляется в Celery."""
    from app.core.config import settings
    from jose import jwt

    token = jwt.encode(
        {"sub": "1", "role": "user", "exp": 9999999999},
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )
    fake_message.text = "Как дела?"

    with patch("app.bot.handlers.get_redis") as mock_redis, \
         patch("app.bot.handlers.llm_request.delay") as mock_delay:
        mock_redis_instance = AsyncMock()
        mock_redis_instance.get.return_value = token
        mock_redis.return_value = mock_redis_instance

        await handle_message(fake_message)

        mock_delay.assert_called_once_with(12345, "Как дела?")
        fake_message.answer.assert_called_once()
