from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

order_item = Table(
    "order_item",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("menu_item_id", Integer, ForeignKey("menu_items.id")),
)


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    available = Column(Boolean, default=True)
    orders = relationship("Order", secondary=order_item,
                          back_populates="items")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="created")  # created, paid, cancelled
    items = relationship("MenuItem", secondary=order_item,
                         back_populates="orders")
