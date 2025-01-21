from db import cursor

from .base_controller import BaseController
from models.reviews import base_review_object
from models.users import base_user_object
from models.products import base_product_object

def create_review_object(review):
    review = base_review_object(review)
    customer_id = review.get("customer_id")
    product_id = review.get("product_id")

    user_query = """SELECT user_id, first_name, last_name, email, active, created_at, updated_at FROM "Users"
    WHERE user_id = %s"""
    cursor.execute(user_query, (customer_id,))
    user = cursor.fetchone()
    user = base_user_object(user)
    review["customer"] = user
    del review["customer_id"]

    product_query = """SELECT * FROM "Products"
    WHERE product_id = %s"""
    cursor.execute(product_query, (product_id,))
    product = cursor.fetchone()
    product = base_product_object(product)
    review["product"] = product
    del review["product_id"]

    return review

class ReviewsController(BaseController):
    table_name = "Reviews"
    post_data_fields = ["customer_id", "product_id", "rating", "comment"]
    default_values = [None, None, 0, "", None]
    return_fields = ["review_id", "customer_id", "product_id", "rating", "comment", "created_at"]
    create_record_object = lambda _, review: create_review_object(review)
