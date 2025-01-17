from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "OrderItems" (
    order_item_id UUID NOT NULL,
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC NOT NULL,
    total_price NUMERIC NOT NULL GENERATED ALWAYS AS (quantity * unit_price) STORED,
    PRIMARY KEY (order_item_id),
    FOREIGN KEY (order_id) REFERENCES "Orders" (order_id),
    FOREIGN KEY (product_id) REFERENCES "Products" (product_id)
)""")

connection.commit()