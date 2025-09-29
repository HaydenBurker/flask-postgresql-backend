from db import connection, cursor

from .base_model import Model

class Shipping(Model):
    primary_key = "shipping_id"
    tablename = "Shippings"

    def __init__(self, shipping_id=None, order_id=None, shipping_address="", shipping_label="", shipping_cost=0, tracking_number="", shipping_status="", shipped_date=None):
        self.shipping_id = shipping_id
        self.order_id = order_id
        self.shipping_address = shipping_address
        self.shipping_label = shipping_label
        self.shipping_cost = shipping_cost
        self.tracking_number = tracking_number
        self.shipping_status = shipping_status
        self.shipped_date = shipped_date

    @classmethod
    def init_model(cls):
        super().init_model()

        cursor.execute("""CREATE TABLE IF NOT EXISTS "Shippings" (
            shipping_id UUID NOT NULL,
            order_id UUID NOT NULL UNIQUE,
            shipping_address VARCHAR NOT NULL,
            shipping_label VARCHAR NOT NULL,
            shipping_cost NUMERIC NOT NULL,
            tracking_number VARCHAR NOT NULL,
            shipping_status VARCHAR NOT NULL,
            shipped_date TIMESTAMP WITH TIME ZONE NOT NULL,
            PRIMARY KEY (shipping_id),
            FOREIGN KEY (order_id) REFERENCES "Orders" (order_id) ON DELETE CASCADE
        )""")

        connection.commit()

Shipping.init_model()
