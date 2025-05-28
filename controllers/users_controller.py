from flask import jsonify

from db import cursor
from .base_controller import BaseController

from models.product_suppliers import base_product_supplier_object
from models.order_items import base_order_item_object
from models.categories import base_category_object
from models.discounts import base_discount_object
from models.shippings import base_shipping_object
from models.suppliers import base_supplier_object
from models.payments import base_payment_object
from models.products import base_product_object
from models.reviews import base_review_object
from models.orders import base_order_object
from models.users import User, base_user_object

from util.records import create_record_mapping
from util.validate_uuid import validate_uuid4


def create_user_object(user_data, many=False):
    users = [base_user_object(user) for user in user_data] if many else [base_user_object(user_data)]
    user_ids = tuple(set(user["user_id"] for user in users))

    reviews = []
    if user_ids:
        reviews_query = """SELECT review_id, customer_id, product_id, rating, comment, created_at FROM "Reviews"
        WHERE customer_id IN %s"""
        cursor.execute(reviews_query, (user_ids,))
        reviews = cursor.fetchall()
    user_reviews_mapping = create_record_mapping(reviews, base_review_object, key="customer_id", many=True)

    products = []
    if user_ids:
        review_product_ids = tuple(set(review[2] for review in reviews))
        products_query = """SELECT * FROM "Products"
        WHERE created_by_id IN %s OR product_id IN %s"""
        cursor.execute(products_query, (user_ids, review_product_ids or user_ids))
        products = cursor.fetchall()
    user_product_mapping = create_record_mapping(products, base_product_object, key="created_by_id", many=True)
    product_product_mapping = create_record_mapping(products, base_product_object, key="product_id")
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

    discounts = []
    if order_ids:
        discounts_query = """SELECT "Discounts".discount_id, "Discounts".discount_code, "Discounts".discount_type, "Discounts".discount_value, "Discounts".start_date, "Discounts".end_date, "Discounts".min_order_amount, "OrdersDiscountsXref".order_id FROM "Discounts"
        INNER JOIN "OrdersDiscountsXref" ON "OrdersDiscountsXref".discount_id = "Discounts".discount_id
        WHERE order_id IN %s"""
        cursor.execute(discounts_query, (order_ids,))
        discounts = cursor.fetchall()
    order_discounts_mapping = create_record_mapping(discounts, base_discount_object, many=True)

    order_items = []
    if order_ids:
        order_items_query = """SELECT * FROM "OrderItems"
        WHERE order_id IN %s"""
        cursor.execute(order_items_query, (order_ids,))
        order_items = cursor.fetchall()
    order_order_items_mapping = create_record_mapping(order_items, base_order_item_object, key="order_id", many=True)

    product_suppliers = []
    if product_ids:
        product_supplier_query = """SELECT * FROM "ProductSuppliers"
        WHERE product_id IN %s"""
        cursor.execute(product_supplier_query, (product_ids,))
        product_suppliers = cursor.fetchall()
    supplier_product_supplier_mapping = create_record_mapping(product_suppliers, base_product_supplier_object, key="product_id", many=True)

    supplier_ids = set()
    for product_suppliers in supplier_product_supplier_mapping.values():
        supplier_ids.update(product_supplier["supplier_id"] for product_supplier in product_suppliers)

    if supplier_ids:
        suppliers_query = """SELECT * FROM "Suppliers"
        WHERE supplier_id IN %s"""
        cursor.execute(suppliers_query, (tuple(supplier_ids),))
        suppliers = cursor.fetchall()
        supplier_product_mapping = create_record_mapping(suppliers, base_supplier_object, key="supplier_id")


    for i, user in enumerate(users):
        user_id = user["user_id"]
        users[i]["products"] = user_product_mapping.get(user_id, [])
        users[i]["orders"] = user_order_mapping.get(user_id, [])
        users[i]["reviews"] = user_reviews_mapping.get(user_id, [])

        for product in users[i]["products"]:
            product_id = product["product_id"]
            product["categories"] = product_category_mapping.get(product_id, [])
            product["product_suppliers"] = supplier_product_supplier_mapping.get(product["product_id"], [])

            del product["created_by_id"]

            for product_supplier in product["product_suppliers"]:
                product_supplier["supplier"] = supplier_product_mapping.get(product_supplier["supplier_id"])
                del product_supplier["product_id"]
                del product_supplier["supplier_id"]

        for order in users[i]["orders"]:
            order_id = order["order_id"]
            order["shipping"] = order_shipping_mapping.get(order_id, None)
            order["payments"] = order_payment_mapping.get(order_id, [])
            order["discounts"] = order_discounts_mapping.get(order_id, [])
            order["order_items"] = order_order_items_mapping.get(order_id, [])

            del order["customer_id"]
            if order["shipping"]:
                del order["shipping"]["order_id"]
            for payment in order["payments"]:
                del payment["order_id"]
            for order_item in order["order_items"]:
                del order_item["order_id"]

        for review in users[i]["reviews"]:
            product_id = review["product_id"]
            review["product"] = product_product_mapping.get(product_id, None)
            del review["customer_id"]
            del review["product_id"]

    return users if many else users[0]

class UsersController(BaseController):
    create_record_object = lambda _, user_data, many=False: [base_user_object(user) for user in user_data] if many else base_user_object(user_data)
    model = User

    def get_nested_records(self, record_id):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400

        get_by_id_query = f"""SELECT * FROM "{self.model.tablename}"
        WHERE {self.model.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()

        record = self.model().load(record)

        if not record:
            return jsonify({"message": "record not found"}), 404

        return jsonify({"message": "record found", "results": create_user_object(record.dump().values())}), 200
