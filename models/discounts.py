from db import connection, cursor

from util.records import base_record_object

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

def base_discount_object(discount):
    return base_record_object(discount, ["discount_id", "discount_code", "discount_type", "discount_value", "start_date", "end_date", "min_order_amount"])
