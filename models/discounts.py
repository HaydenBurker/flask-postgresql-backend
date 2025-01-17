from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Discounts" (
    discount_id UUID NOT NULL,
    discount_code VARCHAR NOT NULL,
    discount_type VARCHAR,
    discount_value NUMERIC NOT NULL,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    min_order_amount INTEGER,
    PRIMARY KEY (discount_id)
)""")

connection.commit()