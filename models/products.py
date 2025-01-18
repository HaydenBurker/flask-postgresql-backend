from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Products" (
    product_id UUID NOT NULL,
    name VARCHAR NOT NULL UNIQUE,
    description VARCHAR,
    price NUMERIC NOT NULL,
    stock_quantity INTEGER NOT NULL,
    created_by_id UUID,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    UNIQUE (name),
    PRIMARY KEY (product_id),
    FOREIGN KEY (created_by_id) REFERENCES "Users" (user_id) ON DELETE SET NULL
)""")

connection.commit()

def base_product_object(product):
    [product_id, name, description, price, stock_quantity, created_by_id, created_at, updated_at] = product
    return {
        "product_id": product_id,
        "name": name,
        "description": description,
        "price": price,
        "stock_quantity": stock_quantity,
        "created_by_id": created_by_id,
        "created_at": str(created_at),
        "updated_at": str(updated_at)
    }
