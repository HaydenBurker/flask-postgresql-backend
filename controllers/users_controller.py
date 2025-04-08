from db import cursor
from .base_controller import BaseController
from models.users import base_user_object
from models.products import base_product_object
from util.records import create_record_mapping


def create_user_object(user_data, many=False):
    users = [base_user_object(user) for user in user_data] if many else [base_user_object(user_data)]
    user_ids = tuple([user["user_id"] for user in users])

    if user_ids:
        products_query = """SELECT * FROM "Products"
        WHERE created_by_id in %s"""
        cursor.execute(products_query, (user_ids,))
        products = cursor.fetchall()
        user_product_mapping = create_record_mapping(products, base_product_object, key="created_by_id", many=True)

        for i, user in enumerate(users):
            user_id = user["user_id"]
            users[i]["products"] = user_product_mapping.get(user_id, [])

    return users if many else users[0]

class UsersController(BaseController):
    table_name = "Users"
    post_data_fields = ["first_name", "last_name", "email", "password", "active"]
    default_values = ["", "", "", "", True, None, None]
    return_fields = ["user_id", "first_name", "last_name", "email", "active", "created_at", "updated_at"]
    create_record_object = lambda _, user, many=False: create_user_object(user, many)
