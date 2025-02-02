from db import cursor
from .base_controller import BaseController
from models.users import base_user_object
from models.products import base_product_object


def create_user_object(user, many=False):
    users = [base_user_object(u) for u in user] if many else base_user_object(user)
    user_ids = tuple([user["user_id"] for user in users]) if many == True else users.get("user_id")

    if user_ids:
        products_query = f"""SELECT * FROM "Products"
        WHERE created_by_id {"IN" if many else "="} %s"""
        cursor.execute(products_query, (user_ids,))
        products = cursor.fetchall()
        products = [base_product_object(product) for product in products]
        user_products = {product.get("created_by_id"): [] for product in products}
        for product in products:
            user_products[product.get("created_by_id")].append(product)

    if many:
        for i, user in enumerate(users):
            users[i]["products"] = user_products.get(user["user_id"], [])
    else:
        users["products"] = user_products.get(users["user_id"], [])
    return users

class UsersController(BaseController):
    table_name = "Users"
    post_data_fields = ["first_name", "last_name", "email", "password", "active"]
    default_values = ["", "", "", "", True, None, None]
    return_fields = ["user_id", "first_name", "last_name", "email", "active", "created_at", "updated_at"]
    create_record_object = lambda _, user, many=False: create_user_object(user, many)
