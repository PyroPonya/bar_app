import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database import Base, get_db
from app.main import app

# Используем SQLite in-memory для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestAsyncSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    """Один event loop на всю сессию тестов."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    """Создаёт таблицы перед тестами, удаляет после."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
async def db_session():
    """Сессия БД для каждого теста."""
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session):
    """HTTP клиент с подменой зависимости get_db и моком RabbitMQ."""
    # Подменяем зависимость БД
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Мокаем RabbitMQ
    with patch("app.rabbitmq.publish_order_event", new_callable=AsyncMock) as mock_rabbit:
        from httpx import AsyncClient, ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            client.mock_rabbit = mock_rabbit
            yield client

    app.dependency_overrides.clear()

    # Очищаем моки
    mock_rabbit.reset_mock()
