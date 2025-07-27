from db import connection, cursor

from .base_model import Model

class ProductCategory(Model):
    tablename = "ProductsCategoriesXref"

    def __init__(self, product_id=None, category_id=None):
        self.product_id = product_id
        self.category_id = category_id
        self.set_fields()

cursor.execute("""CREATE TABLE IF NOT EXISTS "ProductsCategoriesXref" (
    product_id UUID NOT NULL,
    category_id UUID NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES "Products" (product_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES "Categories" (category_id) ON DELETE CASCADE
)""")

connection.commit()
