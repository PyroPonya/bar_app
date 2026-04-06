import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_order(client: AsyncClient):
    # Создаём блюдо
    resp = await client.post("/menu/", json={"name": "Вино", "price": 5.0})
    assert resp.status_code == 201
    item_id = resp.json()["id"]

    # Создаём заказ
    resp2 = await client.post("/orders/", json={"item_ids": [item_id]})
    assert resp2.status_code == 201
    order = resp2.json()
    assert order["status"] == "created"
    assert len(order["items"]) == 1
    assert order["items"][0]["name"] == "Вино"
