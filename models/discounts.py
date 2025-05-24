from db import connection, cursor

from util.records import base_record_object
from .base_model import Model

class Discount(Model):
    primary_key = "discount_id"
    tablename = "Discounts"

    def __init__(self, discount_id=None, discount_code="", discount_type="", discount_value=0, start_date=None, end_date=None, min_order_amount=0):
        self.discount_id  = discount_id
        self.discount_code  = discount_code
        self.discount_type  = discount_type
        self.discount_value  = discount_value
        self.start_date  = start_date
        self.end_date  = end_date
        self.min_order_amount  = min_order_amount

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
