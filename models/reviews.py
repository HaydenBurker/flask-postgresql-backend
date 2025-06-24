from db import connection, cursor

from .base_model import Model

class Review(Model):
    primary_key = "review_id"
    tablename = "Reviews"

    def __init__(self, review_id=None, customer_id=None, product_id=None, rating=0, comment="", created_at=None):
        self.review_id = review_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
        self.set_fields()

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
