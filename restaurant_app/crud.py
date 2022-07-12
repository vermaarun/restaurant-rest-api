import uuid

from sqlalchemy.orm import Session
from sqlalchemy import and_

from . import models, schemas


# Item
def create_item(db: Session, item: schemas.Item):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session):
    return db.query(models.Item).all()


def get_item_by_id(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()


def get_item_by_name(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name == name).first()


def delete_item_by_id(db: Session, id: int):
    db.query(models.Item).filter(models.Item.id == id).delete()
    db.commit()


def update_item_by_id(db: Session,
                      db_item: schemas.Item,
                      item: schemas.ItemUpdate
                      ):
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)


# Table
def create_table(db: Session, table: schemas.Table):
    db_table = models.Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


def get_table_by_id(db: Session, id: int):
    return db.query(models.Table).filter(models.Table.id == id).first()


def get_tables(db: Session):
    return db.query(models.Table).all()


def update_table_by_id():
    pass


def delete_table_by_id(db: Session, id: int):
    db.query(models.Table).filter(models.Table.id == id).delete()
    db.commit()


# Order
def add_item_to_table(item: schemas.Item, table_id: int, db: Session):
    db_order = models.OrderDetail(table_id=table_id,
                                  item_name=item.name,
                                  item_price=item.price
                                  )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)


def get_order_by_order_id(db: Session, order_id: str):
    return db.query(models.OrderDetail).filter(
        models.OrderDetail.order_id == order_id
    ).all()


def delete_item_from_table(db: Session, table_id: int, item_id: int):
    db.query(models.OrderDetail).filter(and_(
        models.OrderDetail.table_id == table_id,
        models.OrderDetail.item_id == item_id,
        models.OrderDetail.order_id == "0000"
    )).delete()
    db.commit()


def place_order(db: Session, table_id: int):
    db_items = (
        db.query(
            models.OrderDetail
        ).filter(and_(models.OrderDetail.table_id == table_id,
                      models.OrderDetail.order_id == "0000")).all()
    )

    if db_items:
        order_id = str(uuid.uuid4())
    else:
        return None
    for db_item in db_items:
        setattr(db_item, "order_id", order_id)
    db.add_all(db_items)
    db.commit()

    order_status = models.OrderStatus(order_id=order_id,
                                      table_id=table_id,
                                      status="In Progress"
                                      )
    db.add(order_status)
    db.commit()
    db.refresh(order_status)
    return order_id


def get_current_order_by_table_id(db: Session, table_id: int):
    return db.query(models.OrderStatus).filter(
        and_(
            models.OrderStatus.table_id == table_id,
            models.OrderStatus.status == "In Progress"
        )
    ).all()


def clean_table():    # make ready for next customer
    pass
