from db import connection, cursor

from .base_model import Model

class OrderDiscount(Model):
    tablename = "OrdersDiscountsXref"

    def __init__(self, order_id=None, discount_id=None):
        self.order_id = order_id
        self.discount_id = discount_id
        self.set_fields()

cursor.execute("""CREATE TABLE IF NOT EXISTS "OrdersDiscountsXref" (
    order_id UUID NOT NULL,
    discount_id UUID NOT NULL,
    PRIMARY KEY (order_id, discount_id),
    FOREIGN KEY (order_id) REFERENCES "Orders" (order_id) ON DELETE CASCADE,
    FOREIGN KEY (discount_id) REFERENCES "Discounts" (discount_id) ON DELETE CASCADE
)""")

connection.commit()