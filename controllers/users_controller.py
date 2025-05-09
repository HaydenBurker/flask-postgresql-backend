from db import cursor
from .base_controller import BaseController
from models.users import base_user_object
from models.products import base_product_object
from models.categories import base_category_object
from models.orders import base_order_object
from models.shippings import base_shipping_object
from models.payments import base_payment_object
from models.product_suppliers import base_product_supplier_object
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
    order_ids = tuple(set(order[0] for order in orders))

    shippings = []
    if order_ids:
        shippings_query = """SELECT shipping_id, order_id, shipping_address, shipping_label, shipping_cost, tracking_number, shipping_status, shipped_date FROM "Shippings"
        WHERE order_id IN %s"""
        cursor.execute(shippings_query, (order_ids,))
        shippings = cursor.fetchall()
    order_shipping_mapping = create_record_mapping(shippings, base_shipping_object, key="order_id")

    payments = []
    if order_ids:
        payments_query = """SELECT payment_id, order_id, payment_method, payment_date, payment_status, payment_amount FROM "Payments"
        WHERE order_id IN %s"""
        cursor.execute(payments_query, (order_ids,))
        payments = cursor.fetchall()
    order_payment_mapping = create_record_mapping(payments, base_payment_object, key="order_id", many=True)

    product_suppliers = []
    if product_ids:
        product_supplier_query = """SELECT * FROM "ProductSuppliers"
        WHERE product_id IN %s"""
        cursor.execute(product_supplier_query, (product_ids,))
        product_suppliers = cursor.fetchall()
    supplier_product_supplier_mapping = create_record_mapping(product_suppliers, base_product_supplier_object, key="product_id", many=True)

    for i, user in enumerate(users):
        user_id = user["user_id"]
        users[i]["products"] = user_product_mapping.get(user_id, [])
        users[i]["orders"] = user_order_mapping.get(user_id, [])

        for product in users[i]["products"]:
            product_id = product["product_id"]
            product["categories"] = product_category_mapping.get(product_id, [])
            product["suppliers"] = supplier_product_supplier_mapping.get(product["product_id"], [])

            del product["created_by_id"]

            for supplier in product["suppliers"]:
                del supplier["product_id"]

        for order in users[i]["orders"]:
            order_id = order["order_id"]
            order["shipping"] = order_shipping_mapping.get(order_id, None)
            order["payments"] = order_payment_mapping.get(order_id, [])

            del order["customer_id"]
            if order["shipping"]:
                del order["shipping"]["order_id"]
            for payment in order["payments"]:
                del payment["order_id"]

    return users if many else users[0]

class UsersController(BaseController):
    table_name = "Users"
    post_data_fields = ["first_name", "last_name", "email", "password", "active"]
    default_values = ["", "", "", "", True, None, None]
    return_fields = ["user_id", "first_name", "last_name", "email", "active", "created_at", "updated_at"]
    create_record_object = lambda _, user, many=False: create_user_object(user, many)
