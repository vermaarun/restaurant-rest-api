from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    available = Column(Boolean, default=True)


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer, default=1)
    occupied = Column(Boolean, default=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    paid = Column(Boolean, default=False)
    table_id = relationship("Table")
    items = relationship("Item")
