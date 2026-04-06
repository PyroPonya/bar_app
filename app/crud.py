from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas


async def get_menu(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список блюд меню."""
    result = await db.execute(select(models.MenuItem).offset(skip).limit(limit))
    return result.scalars().all()


async def create_menu_item(db: AsyncSession, item: schemas.MenuItemCreate):
    """Создать новое блюдо в меню."""
    db_item = models.MenuItem(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_order(db: AsyncSession, order_id: int):
    """Получить заказ по ID с подгрузкой связанных блюд (eager loading)."""
    result = await db.execute(
        select(models.Order)
        .where(models.Order.id == order_id)
        .options(selectinload(models.Order.items))
    )
    return result.scalar_one_or_none()


async def create_order(db: AsyncSession, item_ids: list[int]):
    """Создать новый заказ из списка ID блюд."""
    # Загружаем все запрошенные блюда
    items = []
    for iid in item_ids:
        res = await db.execute(select(models.MenuItem).where(models.MenuItem.id == iid))
        item = res.scalar_one_or_none()
        if item:
            items.append(item)

    # Создаём заказ
    order = models.Order(items=items, status="created")
    db.add(order)
    await db.commit()
    await db.refresh(order)

    # Принудительно подгружаем items после коммита (eager loading)
    # Это необходимо, чтобы Pydantic мог сериализовать order.items без ошибки MissingGreenlet
    result = await db.execute(
        select(models.Order)
        .where(models.Order.id == order.id)
        .options(selectinload(models.Order.items))
    )
    order = result.scalar_one()
    return order
