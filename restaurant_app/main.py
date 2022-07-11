from fastapi import FastAPI

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
def create_item():
    pass


@app.get("/items/{item_id}", response_model=schemas.Item)
def get_item():
    pass


@app.get("/items/", response_model=list[schemas.Item])
def get_items():
    pass


@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item():
    pass


@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item():
    pass


# /tables/ endpoints
@app.post("/tables/", response_model=schemas.Table)
def create_table():
    pass


@app.get("/tables/{table_id}", response_model=schemas.Table)
def get_table():
    pass


@app.get("/tables/", response_model=list[schemas.Table])
def get_tables():
    pass


@app.put("/tables/{table_id}", response_model=schemas.Table)
def update_table():
    pass


@app.delete("/tables/{table_id}", response_model=schemas.Table)
def delete_table():
    pass


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
