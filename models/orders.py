from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Orders" (
    order_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    shipping_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR NOT NULL,
    total_amount VARCHAR NOT NULL,
    active BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES "Users" (user_id)
)""")

connection.commit()