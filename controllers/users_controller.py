from db import cursor
from .base_controller import BaseController
from models.users import base_user_object
from models.products import base_product_object


def create_user_object(user, many=False):
    if many:
        users = [base_user_object(u) for u in user]
        user_ids = tuple([user["user_id"] for user in users])

        if user_ids:
            products_query = """SELECT * FROM "Products"
            WHERE created_by_id IN %s"""
            cursor.execute(products_query, (user_ids,))
            products = cursor.fetchall()
            products = [base_product_object(product) for product in products]
            products = {product["product_id"]: product for product in products}
        else:
            products = []

        for i, user in enumerate(users):
            users[i]["products"] = [product for product in products.values() if product["created_by_id"] == user["user_id"]]
        return users
    else:
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
    create_record_object = lambda _, user, many=False: create_user_object(user, many)
