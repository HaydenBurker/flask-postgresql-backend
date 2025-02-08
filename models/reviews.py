from db import connection, cursor

from util.records import base_record_object

cursor.execute("""CREATE TABLE IF NOT EXISTS "Reviews" (
    review_id UUID NOT NULL,
    customer_id UUID,
    product_id UUID NOT NULL,
    rating DECIMAL NOT NULL,
    comment VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (review_id),
    FOREIGN KEY (customer_id) REFERENCES "Users" (user_id) ON DELETE SET NULL,
    FOREIGN KEY (product_id) REFERENCES "Products" (product_id) ON DELETE CASCADE
)""")

connection.commit()

def base_review_object(review):
    return base_record_object(review, ["review_id", "customer_id", "product_id", "rating", "comment", "created_at"])
