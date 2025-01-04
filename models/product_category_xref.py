from db import get_connection

with get_connection() as [connection, cursor]:
    cursor.execute("""CREATE TABLE IF NOT EXISTS "ProductsCategoriesXref" (
            product_id UUID NOT NULL,
            category_id UUID NOT NULL,
            PRIMARY KEY (product_id, category_id),
            FOREIGN KEY (product_id) REFERENCES "Products" (product_id),
            FOREIGN KEY (category_id) REFERENCES "Categories" (category_id)
    )""")

    connection.commit()
