import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_order():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # создаем блюдо
        await ac.post("/menu/", json={"name": "Вино", "price": 5.0})
        # заказ
        resp = await ac.post("/orders/", json={"item_ids": [1]})
        assert resp.status_code == 201
        order = resp.json()
        assert order["status"] == "created"
        assert len(order["items"]) == 1
