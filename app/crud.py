from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas


async def get_menu(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.MenuItem).offset(skip).limit(limit))
    return result.scalars().all()


async def create_menu_item(db: AsyncSession, item: schemas.MenuItemCreate):
    db_item = models.MenuItem(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    return result.scalar_one_or_none()


async def create_order(db: AsyncSession, item_ids: list[int]):
    # получить все блюда
    items = []
    for iid in item_ids:
        res = await db.execute(select(models.MenuItem).where(models.MenuItem.id == iid))
        item = res.scalar_one_or_none()
        if item:
            items.append(item)
    order = models.Order(items=items, status="created")
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order
