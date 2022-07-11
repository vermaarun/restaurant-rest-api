from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# /items/ endpoints
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.Item, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_name(db, name=item.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already registered")
    return crud.create_item(db=db, item=item)


@app.get("/items/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.get("/items/", response_model=list[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    items = crud.get_items(db=db)
    return items


@app.put("/items/{item_id}")
def update_item(item_id: int,
                item: schemas.ItemUpdate,
                db: Session = Depends(get_db)
                ):
    db_item = crud.get_item_by_id(db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.update_item_by_id(db, db_item=db_item, item=item)
    return {"Item": "Updated"}


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    crud.delete_item_by_id(db, id=item_id)
    return {"ok": True}


# /tables/ endpoints
@app.post("/tables/", response_model=schemas.Table)
def create_table(table: schemas.Table, db: Session = Depends(get_db)):
    db_table = crud.get_table_by_id(db, id=table.id)
    if db_table:
        raise HTTPException(status_code=400, detail="Table already registered")
    return crud.create_table(db=db, table=table)


@app.get("/tables/{table_id}", response_model=schemas.Table)
def get_table(table_id: int, db: Session = Depends(get_db)):
    db_table = crud.get_table_by_id(db, id=table_id)
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return db_table


@app.get("/tables/", response_model=list[schemas.Table])
def get_tables(db: Session = Depends(get_db)):
    tables = crud.get_tables(db=db)
    return tables


@app.put("/tables/{table_id}", response_model=schemas.Table)
def update_table():
    pass


@app.delete("/tables/{table_id}", response_model=schemas.Table)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    crud.delete_table_by_id(db, id=table_id)
    return {"ok": True}


# order related endpoints
@app.post("/tables/{table_id}/items/{item_id}", response_model=schemas.Item)
def add_item_to_table():
    pass


@app.get("/tables/{table_id}/items/", response_model=list[schemas.Item])
def get_order_by_table_id():
    pass


@app.delete("/tables/{table_id}/items/{item_id}", response_model=schemas.Item)
def delete_item_from_table():
    pass


# this endpoint will make table available for next customer
@app.put("/tables/{table_id}/paid")
def update_order_by_table_id():
    pass
