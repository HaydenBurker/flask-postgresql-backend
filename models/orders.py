from db import connection, cursor

from util.records import base_record_object

cursor.execute("""CREATE TABLE IF NOT EXISTS "Orders" (
    order_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    shipping_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR NOT NULL,
    total_amount INTEGER NOT NULL,
    active BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES "Users" (user_id) ON DELETE CASCADE
)""")

connection.commit()

def base_order_object(order):
    return base_record_object(order, ["order_id", "customer_id", "shipping_date", "status", "total_amount", "active", "created_at", "updated_at"])
