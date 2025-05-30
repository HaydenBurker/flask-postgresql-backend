from db import cursor

from .base_controller import BaseController
from models.reviews import Review
from models.users import base_user_object
from models.products import base_product_object
from util.records import create_record_mapping

def create_review_object(review_data, many=False):
    reviews = [review.dump() for review in review_data] if many else [review_data.dump()]
    customer_ids = tuple(set(review["customer_id"] for review in reviews))
    product_ids = tuple(set(review["product_id"] for review in reviews))

    users = []
    if customer_ids:
        users_query = """SELECT user_id, first_name, last_name, email, active, created_at, updated_at FROM "Users"
        WHERE user_id IN %s"""
        cursor.execute(users_query, (customer_ids,))
        users = cursor.fetchall()
    review_user_mapping = create_record_mapping(users, base_user_object, key="user_id")

    products = []
    if product_ids:
        products_query = """SELECT * FROM "Products"
        WHERE product_id IN %s"""
        cursor.execute(products_query, (product_ids,))
        products = cursor.fetchall()
    review_product_mapping = create_record_mapping(products, base_product_object, key="product_id")

    for i, review in enumerate(reviews):
        reviews[i]["customer"] = review_user_mapping.get(review["customer_id"])
        del reviews[i]["customer_id"]

        reviews[i]["product"] = review_product_mapping.get(review["product_id"])
        del reviews[i]["product_id"]

    return reviews if many else reviews[0]

class ReviewsController(BaseController):
    create_record_object = lambda _, review, many=False: create_review_object(review, many)
    model = Review
