from db import connection, cursor

from .categories import create_category_object

cursor.execute("""CREATE TABLE IF NOT EXISTS "Products" (
    product_id UUID NOT NULL,
    name VARCHAR NOT NULL UNIQUE,
    created_by_id UUID,
    UNIQUE (name),
    PRIMARY KEY (product_id),
    FOREIGN KEY (created_by_id) REFERENCES "Users" (user_id)
)""")

connection.commit()

def create_product_object(product):
    [product_id, name, created_by_id] = product
    created_by_user = created_by_id
    categories = []
    if created_by_id:
        create_by_id_query = """SELECT user_id, first_name, last_name, email, active FROM "Users"
        WHERE user_id = %s"""
        cursor.execute(create_by_id_query, (created_by_id,))
        [user_id, first_name, last_name, email, active] = cursor.fetchone()

        created_by_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "active": active
        }
    categories_query = """SELECT "Categories".category_id, "Categories".name FROM "Categories"
    INNER JOIN "ProductsCategoriesXref" ON "ProductsCategoriesXref".category_id = "Categories".category_id
    WHERE "ProductsCategoriesXref".product_id = %s"""
    cursor.execute(categories_query, (product_id,))
    categories = cursor.fetchall()
    categories = [create_category_object(category) for category in categories]
    return {
        "product_id": product_id,
        "name": name,
        "created_by": created_by_user,
        "categories": categories
    }
