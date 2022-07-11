from sqlalchemy.orm import Session

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
def create_table():
    pass


def get_table_by_id():
    pass


def get_tables():
    pass


def update_table_by_id():
    pass


def delete_table_by_id():
    pass


# Order
def add_item_to_table():    # create order
    pass


def get_order_by_table_id():
    pass


def delete_item_from_table():
    pass


def clean_table():    # make ready for next customer
    pass
