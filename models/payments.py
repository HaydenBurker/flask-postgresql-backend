from db import connection, cursor

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