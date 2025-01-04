from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Products" (
    product_id UUID NOT NULL,
    name VARCHAR NOT NULL UNIQUE,
    created_by_id UUID,
    UNIQUE (name),
    PRIMARY KEY (product_id),
    FOREIGN KEY (created_by_id) REFERENCES "Users" (user_id)
)""")

connection.commit()
