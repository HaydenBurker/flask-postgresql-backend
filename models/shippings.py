from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Shippings" (
    shipping_id UUID NOT NULL,
    order_id UUID NOT NULL,
    shipping_address VARCHAR NOT NULL,
    shipping_label VARCHAR NOT NULL,
    shipping_cost NUMERIC NOT NULL,
    tracking_number VARCHAR NOT NULL,
    shipping_status VARCHAR NOT NULL,
    shipped_date TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (shipping_id),
    FOREIGN KEY (order_id) REFERENCES "Orders" (order_id)
)""")

connection.commit()