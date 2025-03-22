from db import connection, cursor

from util.records import base_record_object

cursor.execute("""CREATE TABLE IF NOT EXISTS "Payments" (
    payment_id UUID NOT NULL,
    order_id UUID NOT NULL,
    payment_method VARCHAR NOT NULL,
    payment_date TIMESTAMP WITH TIME ZONE NOT NULL,
    payment_status VARCHAR NOT NULL,
    payment_amount NUMERIC NOT NULL,
    PRIMARY KEY (payment_id),
    FOREIGN KEY (order_id) REFERENCES "Orders" (order_id) ON DELETE CASCADE
)""")

connection.commit()

def base_payment_object(payment):
    return base_record_object(payment, ["payment_id", "order_id", "payment_method", "payment_date", "payment_status", "payment_amount"])
