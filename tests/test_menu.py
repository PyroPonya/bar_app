import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_menu(client: AsyncClient):
    # Создаём блюдо
    resp = await client.post("/menu/", json={"name": "Пиво", "price": 3.5})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Пиво"
    assert data["price"] == 3.5

    # Получаем список меню
    resp2 = await client.get("/menu/")
    assert resp2.status_code == 200
    items = resp2.json()
    assert len(items) == 1
    assert items[0]["name"] == "Пиво"
