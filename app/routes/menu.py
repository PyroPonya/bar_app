from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/", response_model=list[schemas.MenuItemResponse])
async def list_menu(db: AsyncSession = Depends(get_db)):
    return await crud.get_menu(db)


@router.post("/", response_model=schemas.MenuItemResponse, status_code=201)
async def add_item(item: schemas.MenuItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_menu_item(db, item)
