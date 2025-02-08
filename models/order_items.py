from db import connection, cursor

from util.records import base_record_object

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

def base_order_item_object(order_item):
    return base_record_object(order_item, ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "total_price"])
