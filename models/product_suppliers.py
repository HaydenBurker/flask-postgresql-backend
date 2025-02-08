from db import connection, cursor

from util.records import base_record_object

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

def base_product_supplier_object(product_supplier):
    return base_record_object(product_supplier, ["product_id", "supplier_id", "supply_price", "supply_date"])
