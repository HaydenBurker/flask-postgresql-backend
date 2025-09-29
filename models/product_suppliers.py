from db import connection, cursor

from .base_model import Model

class ProductSupplier(Model):
    tablename = "ProductSuppliers"

    def __init__(self, product_id=None, supplier_id=None, supply_price=0, supply_date=None):
        self.product_id = product_id
        self.supplier_id = supplier_id
        self.supply_price = supply_price
        self.supply_date = supply_date

    @classmethod
    def init_model(cls):
        super().init_model()

        cursor.execute("""CREATE TABLE IF NOT EXISTS "ProductSuppliers" (
            product_id UUID NOT NULL,
            supplier_id UUID NOT NULL,
            supply_price NUMERIC NOT NULL,
            supply_date TIMESTAMP WITH TIME ZONE,
            PRIMARY KEY (product_id, supplier_id),
            FOREIGN KEY (product_id) REFERENCES "Products" (product_id) ON DELETE CASCADE,
            FOREIGN KEY (supplier_id) REFERENCES "Suppliers" (supplier_id) ON DELETE CASCADE
        )""")

        connection.commit()

ProductSupplier.init_model()
