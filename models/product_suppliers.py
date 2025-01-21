from db import connection, cursor

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
    [product_id, supplier_id, supply_price, supply_date] = product_supplier

    return {
        "product_id": product_id,
        "supplier_id": supplier_id,
        "supply_price": supply_price,
        "supply_date": supply_date and supply_date.isoformat()
    }
