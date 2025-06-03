from db import connection, cursor

from util.records import base_record_object
from .base_model import Model

class Order(Model):
    primary_key = "order_id"
    tablename = "Orders"

    def __init__(self, order_id=None, customer_id=None, order_date=None, shipping_date=None, status="", total_amount=0, active=True, created_at=None, updated_at=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date
        self.shipping_date = shipping_date
        self.status = status
        self.total_amount = total_amount
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at
        self.set_fields()

cursor.execute("""CREATE TABLE IF NOT EXISTS "Orders" (
    order_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    order_date TIMESTAMP WITH TIME ZONE,
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
    return base_record_object(order, ["order_id", "customer_id", "order_date", "shipping_date", "status", "total_amount", "active", "created_at", "updated_at"])
