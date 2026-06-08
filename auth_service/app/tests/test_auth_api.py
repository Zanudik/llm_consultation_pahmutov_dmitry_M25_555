"""
Интеграционные тесты: регистрация, логин, профиль.
"""
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.db.base import Base
from app.api.deps import get_db
from app.main import create_app

# In-memory SQLite для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


async def override_get_db():
    """Подменяет реальную БД на тестовую."""
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
async def setup_db():
    """Создаёт таблицы перед каждым тестом."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    """Тестовый HTTP-клиент."""
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_register_success(client):
    """Успешная регистрация возвращает 201."""
    response = await client.post("/auth/register", json={
        "email": "test@email.com",
        "password": "123456",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@email.com"
    assert data["role"] == "user"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate(client):
    """Повторная регистрация с тем же email возвращает 409."""
    await client.post("/auth/register", json={
        "email": "dup@email.com",
        "password": "123456",
    })
    response = await client.post("/auth/register", json={
        "email": "dup@email.com",
        "password": "123456",
    })
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client):
    """Успешный логин возвращает 200 и токен."""
    await client.post("/auth/register", json={
        "email": "login@email.com",
        "password": "123456",
    })
    response = await client.post("/auth/login", data={
        "username": "login@email.com",
        "password": "123456",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """Неверный пароль возвращает 401."""
    await client.post("/auth/register", json={
        "email": "wrong@email.com",
        "password": "123456",
    })
    response = await client.post("/auth/login", data={
        "username": "wrong@email.com",
        "password": "wrongpass",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_token(client):
    """Профиль доступен с валидным токеном."""
    await client.post("/auth/register", json={
        "email": "me@email.com",
        "password": "123456",
    })
    login_resp = await client.post("/auth/login", data={
        "username": "me@email.com",
        "password": "123456",
    })
    token = login_resp.json()["access_token"]

    response = await client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@email.com"


@pytest.mark.asyncio
async def test_me_without_token(client):
    """Без токена возвращает 401."""
    response = await client.get("/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_invalid_token(client):
    """С неверным токеном возвращает 401."""
    response = await client.get("/auth/me", headers={
        "Authorization": "Bearer garbage_token",
    })
    assert response.status_code == 401
