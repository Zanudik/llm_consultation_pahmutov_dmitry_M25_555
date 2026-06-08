# llm-consultation

Двухсервисная система LLM-консультаций. Auth Service (FastAPI) отвечает за регистрацию и выдачу JWT. Bot Service (aiogram + Celery + RabbitMQ + Redis) принимает запросы через Telegram-бота, проверяет JWT и отправляет запросы к LLM через OpenRouter.

## Установка и запуск

### 1. Установить uv
```bash
pip install uv
```
### 2. Клонировать проект и перейти в папку
```bash
git clone https://github.com/Zanudik/llm_consultation_pahmutov_dmitry_M25_555.git
cd llm_consultation_pahmutov_dmitry_M25_555
```
### 3. Установить Docker и запустить RabbitMQ + Redis
```bash
sudo docker compose up -d
```
### 4. Auth Service
```bash
cd auth_service
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Swagger-документация доступна по адресу: http://localhost:8000/docs

### 5. Bot Service
```bash
cd bot_service
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
pip install aiohttp-socks
```
Добавить IP Telegram в hosts (если DNS заблокирован):

```bash
echo "149.154.167.220 api.telegram.org" | sudo tee -a /etc/hosts
```
Запуск Celery worker (терминал 2):

```bash
cd bot_service
source .venv/bin/activate
celery -A app.infra.celery_app worker --loglevel=info
```
Запуск бота (терминал 3):

```bash
cd bot_service
source .venv/bin/activate
python -c "
import asyncio
from app.bot.dispatcher import create_bot, create_dispatcher

async def main():
    bot = create_bot()
    dp = create_dispatcher()
    print('Бот запущен!')
    await dp.start_polling(bot)

asyncio.run(main())
"
```
### 6. Настроить .env
Создать файлы .env в auth_service/ и bot_service/.

auth_service/.env:

```text
APP_NAME=auth-service
ENV=local

JWT_SECRET=change_me_super_secret
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SQLITE_PATH=./auth.db
```
bot_service/.env:

```text
APP_NAME=bot-service
ENV=local

TELEGRAM_BOT_TOKEN=ваш_токен_бота

JWT_SECRET=change_me_super_secret
JWT_ALG=HS256

REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672//

OPENROUTER_API_KEY=ваш_ключ_openrouter
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=liquid/lfm-2.5-1.2b-instruct:free
OPENROUTER_SITE_URL=https://example.com
OPENROUTER_APP_NAME=bot-service
```
API-ключ OpenRouter можно получить на openrouter.ai.
Токен Telegram-бота — у @BotFather.

## Использование
Зарегистрироваться и получить JWT в Swagger Auth Service (POST /auth/register, POST /auth/login)

Отправить токен Telegram-боту командой: /token <jwt>

Задавать вопросы — бот принимает запрос, отправляет в очередь Celery, получает ответ от LLM и возвращает пользователю

## Тесты
```bash
# Auth Service (9 тестов)
cd auth_service && source .venv/bin/activate && python -m pytest app/tests/ -v

# Bot Service (5 тестов)
cd bot_service && source .venv/bin/activate && python -m pytest app/tests/ -v
```

Структура проекта
```text
llm-consultation/
├── auth_service/
│   ├── app/
│   │   ├── api/            # Роутеры и зависимости
│   │   ├── core/           # Конфигурация,
│   │   ├── db/             # Модели
│   │   ├── repositories/   # Доступ к данным
│   │   ├── schemas/        # Pydantic-схемы
│   │   ├── tests/          # Тесты
│   │   └── usecases/       # Бизнес-логика
│   └── pyproject.toml
├── bot_service/
│   ├── app/
│   │   ├── bot/            # Telegram handlers и dispatcher
│   │   ├── core/           # Конфигурация
│   │   ├── infra/          # Redis
│   │   ├── services/       # OpenRouter клиент
│   │   ├── tasks/          # Celery-задачи
│   │   └── tests/          # Тесты
│   └── pyproject.toml
├── docker-compose.yml
├── screenshots/
└── README.md
```

## Демонстрация работы
1. Регистрация пользователя
![Регистрация](screenshots/auth_register_1.png)
![Регистрация](screenshots/auth_register_2.png)

2. Логин
![Логин](screenshots/auth_login_1.png)
![Логин](screenshots/auth_login_2.png)

3. Профиль пользователя
![Профиль](screenshots/auth_me.png)

4. Передача токена Telegram-боту
![Передача](screenshots/telegram_token.png)

5. Запрос к LLM и ответ
![Запрос](screenshots/telegram_chat.png)

6. RabbitMQ — очереди Celery
![RabbitMQ](screenshots/rabbitmq.png)

7. Тесты Auth Service
![Тесты](screenshots/tests_auth.png)

8. Тесты Bot Service
![Тесты](screenshots/tests_bot.png)