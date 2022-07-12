from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


class Detail(BaseModel):
    detail: str


app = FastAPI(title="Simple Restaurant API")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# /items/ endpoints
@app.post("/items/",
          response_model=schemas.Item,
          responses={409: {"model": Detail}},
          tags=["items"],
          )
def create_item(item: schemas.Item, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_name(db, name=item.name)
    if db_item:
        raise HTTPException(status_code=409, detail="Item already registered")
    return crud.create_item(db=db, item=item)


@app.get("/items/{item_id}",
         response_model=schemas.Item,
         tags=["items"],
         )
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.get("/items/",
         response_model=list[schemas.Item],
         tags=["items"],
         )
def get_items(db: Session = Depends(get_db)):
    items = crud.get_items(db=db)
    return items


@app.put("/items/{item_id}",
         tags=["items"],
         )
def update_item(item_id: int,
                item: schemas.ItemUpdate,
                db: Session = Depends(get_db)
                ):
    db_item = crud.get_item_by_id(db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.update_item_by_id(db, db_item=db_item, item=item)
    return {"Item": "Updated"}


@app.delete("/items/{item_id}",
            status_code=204,
            tags=["items"],
            )
def delete_item(item_id: int, db: Session = Depends(get_db)):
    crud.delete_item_by_id(db, id=item_id)


# /tables/ endpoints
@app.post("/tables/",
          response_model=schemas.Table,
          responses={409: {"model": Detail}},
          tags=["tables"],
          )
def create_table(table: schemas.Table, db: Session = Depends(get_db)):
    db_table = crud.get_table_by_id(db, id=table.id)
    if db_table:
        raise HTTPException(status_code=409, detail="Table already registered")
    return crud.create_table(db=db, table=table)


@app.get("/tables/{table_id}",
         response_model=schemas.Table,
         tags=["tables"],
         )
def get_table(table_id: int, db: Session = Depends(get_db)):
    db_table = crud.get_table_by_id(db, id=table_id)
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return db_table


@app.get("/tables/",
         response_model=list[schemas.Table],
         tags=["tables"],
         )
def get_tables(db: Session = Depends(get_db)):
    tables = crud.get_tables(db=db)
    return tables


@app.put("/tables/{table_id}",
         response_model=schemas.Table,
         include_in_schema=False,
         )
def update_table():
    pass


@app.delete("/tables/{table_id}",
            status_code=204,
            tags=["tables"],
            )
def delete_table(table_id: int, db: Session = Depends(get_db)):
    crud.delete_table_by_id(db, id=table_id)


# order related endpoints
@app.post("/tables/{table_id}/items/{item_id}",
          tags=["tables"],
          )
def add_item_to_table(table_id: int,
                      item_id: int,
                      db: Session = Depends(get_db)
                      ):
    # 1. check if item exist
    db_item = crud.get_item_by_id(db=db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    # 2. check if table exist
    db_table = crud.get_table_by_id(db=db, id=table_id)
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    crud.add_item_to_table(db_item, table_id, db)
    return {"Item": "Added"}


@app.delete("/tables/{table_id}/items/{item_id}",
            status_code=204,
            tags=["tables"],
            )
def delete_item_from_table(
        table_id: int,
        item_id: int,
        db: Session = Depends(get_db)
        ):
    # you can only delete the item that has not been placed
    # contact staff in case you want to delete placed item
    crud.delete_item_from_table(db=db, table_id=table_id, item_id=item_id)


@app.post("/orders/tables/{table_id}",
          tags=["orders"],
          )
def create_order_for_table(table_id: int, db: Session = Depends(get_db)):
    order_id = crud.place_order(db=db, table_id=table_id)
    return {"order id": order_id}


@app.get("/orders/{order_id}",
         response_model=list[schemas.OrderDetail],
         tags=["orders"],
         )
def get_order_by_order_id(order_id: str, db: Session = Depends(get_db)):
    orders = crud.get_order_by_order_id(db=db, order_id=order_id)
    return orders


@app.get("/orders/tables/{order_id}",
         tags=["orders"],
         )
def get_current_order_by_table_id(
        table_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_current_order_by_table_id(db=db, table_id=table_id)


# this endpoint will mark the current order by table id as paid
@app.put("/tables/{table_id}/paid", include_in_schema=False)
def update_order_by_table_id(table_id: int, db: Session = Depends(get_db)):
    crud.mark_order_paid(db=db, table_id=table_id)
    return {"message": "Thank you for visiting!!"}
