from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "OrdersDiscountsXref" (
    order_id UUID NOT NULL,
    discount_id UUID NOT NULL,
    PRIMARY KEY (order_id, discount_id),
    FOREIGN KEY (order_id) REFERENCES "Orders" (order_id) ON DELETE CASCADE,
    FOREIGN KEY (discount_id) REFERENCES "Discounts" (discount_id) ON DELETE CASCADE
)""")

connection.commit()