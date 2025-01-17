from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Reviews" (
    review_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    product_id UUID NOT NULL,
    rating DECIMAL NOT NULL,
    comment VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (review_id),
    FOREIGN KEY (customer_id) REFERENCES "Users" (user_id),
    FOREIGN KEY (product_id) REFERENCES "Products" (product_id)
)""")

connection.commit()