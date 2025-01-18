from db import cursor
from .base_controller import BaseController
from models.users import base_user_object
from models.products import base_product_object


def create_user_object(user):
    user = base_user_object(user)
    user_id = user.get("user_id")
    products = []

    products_query = """SELECT * FROM "Products"
    WHERE created_by_id = %s"""
    cursor.execute(products_query, (user_id,))
    products = cursor.fetchall()
    products = [base_product_object(product) for product in products]

    user["products"] = products
    return user

class UsersController(BaseController):
    table_name = "Users"
    post_data_fields = ["first_name", "last_name", "email", "password", "active"]
    default_values = ["", "", "", "", True, None, None]
    return_fields = ["user_id", "first_name", "last_name", "email", "active", "created_at", "updated_at"]
    create_record_object = lambda _, user: create_user_object(user)
