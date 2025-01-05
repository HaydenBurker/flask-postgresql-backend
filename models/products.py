from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Products" (
    product_id UUID NOT NULL,
    name VARCHAR NOT NULL UNIQUE,
    created_by_id UUID,
    UNIQUE (name),
    PRIMARY KEY (product_id),
    FOREIGN KEY (created_by_id) REFERENCES "Users" (user_id) ON DELETE SET NULL
)""")

connection.commit()

def base_product_object(product):
    [product_id, name, created_by_id] = product
    return {
        "product_id": product_id,
        "name": name,
        "created_by_id": created_by_id
    }
