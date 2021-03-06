from typing import Union

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    price: float
    available: Union[bool, None] = True

    class Config:
        orm_mode = True


class ItemUpdate(BaseModel):
    id: int = None
    name: str = None
    price: float = None
    available: Union[bool, None] = True

    class Config:
        orm_mode = True


class Table(BaseModel):
    id: int
    capacity: int
    occupied: Union[bool, None] = False

    class Config:
        orm_mode = True


class OrderDetail(BaseModel):
    id: int
    table_id: int
    # paid: Union[bool, None] = False
    item_name: str
    item_price: float
    order_id: str = None

    class Config:
        orm_mode = True
