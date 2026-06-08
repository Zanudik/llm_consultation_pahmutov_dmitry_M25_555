"""
Обработчики сообщений Telegram-бота.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from jose import JWTError, ExpiredSignatureError

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()


@router.message(Command("token"))
async def cmd_token(message: Message):
    """
    Сохраняет JWT-токен пользователя в Redis.
    Формат: /token <jwt>
    """
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /token <ваш_jwt_токен>")
        return

    token = parts[1].strip()

    # Проверяем, что токен валидный
    try:
        _ = decode_and_validate(token)
    except ExpiredSignatureError:
        await message.answer("Токен истёк. Получите новый в Auth Service.")
        return
    except JWTError:
        await message.answer("Неверный токен. Проверьте и попробуйте снова.")
        return

    # Сохраняем токен в Redis
    redis = await get_redis()
    await redis.set(f"token:{message.from_user.id}", token)
    await message.answer("Токен сохранён! Теперь вы можете задавать вопросы.")


@router.message()
async def handle_message(message: Message):
    """
    Обрабатывает обычные сообщения.
    Если токен есть — отправляет запрос к LLM.
    Если токена нет — просит авторизоваться.
    """
    # Проверяем, есть ли токен
    redis = await get_redis()
    token = await redis.get(f"token:{message.from_user.id}")

    if token is None:
        await message.answer(
            "У вас нет токена. Получите его в Auth Service и отправьте командой:\n"
            "/token <ваш_jwt_токен>"
        )
        return

    # Проверяем, что токен ещё валидный
    try:
        decode_and_validate(token)
    except (JWTError, ExpiredSignatureError):
        await message.answer(
            "Токен недействителен или истёк. Получите новый в Auth Service."
        )
        return

    # Отправляем задачу в Celery
    llm_request.delay(message.chat.id, message.text)
    await message.answer("Запрос принят, обрабатываю...")
