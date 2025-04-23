from db import cursor
from .base_controller import BaseController
from models.users import base_user_object
from models.products import base_product_object
from models.categories import base_category_object
from models.orders import base_order_object
from util.records import create_record_mapping


def create_user_object(user_data, many=False):
    users = [base_user_object(user) for user in user_data] if many else [base_user_object(user_data)]
    user_ids = tuple(set(user["user_id"] for user in users))

    products = []
    if user_ids:
        products_query = """SELECT * FROM "Products"
        WHERE created_by_id in %s"""
        cursor.execute(products_query, (user_ids,))
        products = cursor.fetchall()
    user_product_mapping = create_record_mapping(products, base_product_object, key="created_by_id", many=True)
    product_ids = tuple(set(product[0] for product in products))

    categories = []
    if product_ids:
        categories_query = """SELECT "Categories".category_id, "Categories".name, "Categories".description, "ProductsCategoriesXref".product_id FROM "Categories"
        INNER JOIN "ProductsCategoriesXref" ON "ProductsCategoriesXref".category_id = "Categories".category_id
        WHERE "ProductsCategoriesXref".product_id IN %s"""
        cursor.execute(categories_query, (product_ids,))
        categories = cursor.fetchall()
    product_category_mapping = create_record_mapping(categories, base_category_object, many=True)

    orders = []
    if user_ids:
        orders_query = """SELECT order_id, customer_id, order_date, shipping_date, status, total_amount, active, created_at, updated_at FROM "Orders"
        WHERE customer_id IN %s"""
        cursor.execute(orders_query, (user_ids,))
        orders = cursor.fetchall()
    user_order_mapping = create_record_mapping(orders, base_order_object, key="customer_id", many=True)

    for i, user in enumerate(users):
        user_id = user["user_id"]
        users[i]["products"] = user_product_mapping.get(user_id, [])
        users[i]["orders"] = user_order_mapping.get(user_id, [])

        for product in users[i]["products"]:
            product_id = product["product_id"]
            product["categories"] = product_category_mapping.get(product_id, [])

    return users if many else users[0]

class UsersController(BaseController):
    table_name = "Users"
    post_data_fields = ["first_name", "last_name", "email", "password", "active"]
    default_values = ["", "", "", "", True, None, None]
    return_fields = ["user_id", "first_name", "last_name", "email", "active", "created_at", "updated_at"]
    create_record_object = lambda _, user, many=False: create_user_object(user, many)
