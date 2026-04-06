from pydantic import BaseModel
from typing import List, Optional


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    item_ids: List[int]


class OrderResponse(BaseModel):
    id: int
    status: str
    items: List[MenuItemResponse]

    class Config:
        from_attributes = True
