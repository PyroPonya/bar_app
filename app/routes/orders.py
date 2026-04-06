from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, rabbitmq

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=schemas.OrderResponse, status_code=201)
async def create_order(order: schemas.OrderBase, db: AsyncSession = Depends(get_db)):
    new_order = await crud.create_order(db, order.item_ids)
    # Отправляем событие в RabbitMQ
    await rabbitmq.publish_order_event({"order_id": new_order.id, "status": new_order.status, "item_ids": order.item_ids})
    return new_order


@router.get("/{order_id}", response_model=schemas.OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
