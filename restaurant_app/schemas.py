from typing import Union

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    available: Union[bool, None] = True

    class Config:
        orm_mode = True


class Table(BaseModel):
    id: int
    capacity: int
    occupied: Union[bool, None] = False

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: int
    table_id: int
    paid: Union[bool, None] = False
    items: list[Item] = []
