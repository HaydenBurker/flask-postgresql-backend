from db import connection, cursor

from .base_model import Model

class OrderItem(Model):
    primary_key = "order_item_id"
    tablename = "OrderItems"

    def __init__(self, order_item_id=None, order_id=None, product_id=None, quantity=0, unit_price=0, total_price=0):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
        self.set_fields()

    def dump_update(self):
        obj = super().dump_update()
        del obj["total_price"]
        return obj

cursor.execute("""CREATE TABLE IF NOT EXISTS "OrderItems" (
    order_item_id UUID NOT NULL,
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC NOT NULL,
    total_price NUMERIC NOT NULL GENERATED ALWAYS AS (quantity * unit_price) STORED,
    PRIMARY KEY (order_item_id),
    FOREIGN KEY (order_id) REFERENCES "Orders" (order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES "Products" (product_id) ON DELETE CASCADE
)""")

connection.commit()
