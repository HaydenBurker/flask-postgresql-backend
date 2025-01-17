from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "ProductSuppliers" (
    product_id UUID NOT NULL,
    supplier_id UUID NOT NULL,
    supply_price NUMERIC NOT NULL,
    supply_date TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (product_id, supplier_id),
    FOREIGN KEY (product_id) REFERENCES "Products" (product_id),
    FOREIGN KEY (supplier_id) REFERENCES "Suppliers" (supplier_id)
)""")

connection.commit()