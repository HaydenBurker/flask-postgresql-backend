from db import connection, cursor

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

    @classmethod
    def init_model(cls):
        super().init_model()

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

Order.init_model()
