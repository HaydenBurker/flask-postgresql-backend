from db import connection, cursor

from .base_model import Model

class Product(Model):
    primary_key = "product_id"
    tablename = "Products"

    def __init__(self, product_id=None, name="", description="", price=0, stock_quantity=0, created_by_id=None, created_at=None, updated_at=None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.created_by_id = created_by_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.set_fields()

cursor.execute("""CREATE TABLE IF NOT EXISTS "Products" (
    product_id UUID NOT NULL,
    name VARCHAR NOT NULL UNIQUE,
    description VARCHAR,
    price NUMERIC NOT NULL,
    stock_quantity INTEGER NOT NULL,
    created_by_id UUID,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    UNIQUE (name),
    PRIMARY KEY (product_id),
    FOREIGN KEY (created_by_id) REFERENCES "Users" (user_id) ON DELETE SET NULL
)""")

connection.commit()
