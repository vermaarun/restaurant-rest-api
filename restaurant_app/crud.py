from sqlalchemy.orm import Session

from . import models, schemas


# Item
def create_item():
    pass


def get_items():
    pass


def get_item_by_id():
    pass


def delete_item_by_id():
    pass


def update_item_by_id():
    pass


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
