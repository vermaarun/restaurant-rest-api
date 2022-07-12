from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    available = Column(Boolean, default=True)


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer, default=1)
    occupied = Column(Boolean, default=False)


class OrderStatus(Base):
    __tablename__ = "order_status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    table_id = Column(Integer)
    order_id = Column(String)
    status = Column(String)


class OrderDetail(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # paid = Column(Boolean, default=False)
    table_id = Column(Integer)
    item_id = Column(Integer)
    item_name = Column(String)
    item_price = Column(Float)
    order_id = Column(String, default="0000")
