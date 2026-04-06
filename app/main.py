from fastapi import FastAPI
from app.routes import menu, orders
from app.database import engine, Base
from app.rabbitmq import init_rabbitmq
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: создаем таблицы, подключаем RabbitMQ
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_rabbitmq()
    yield
    # shutdown: закрываем соединения
    await engine.dispose()

app = FastAPI(title="Bar API", lifespan=lifespan)

app.include_router(menu.router)
app.include_router(orders.router)
