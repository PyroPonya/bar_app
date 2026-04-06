import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_and_get_menu():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # создаем блюдо
        resp = await ac.post("/menu/", json={"name": "Пиво", "price": 3.5})
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Пиво"
        # получаем список
        resp2 = await ac.get("/menu/")
        assert resp2.status_code == 200
        assert len(resp2.json()) == 1
