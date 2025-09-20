from flask import jsonify

from db import cursor
from .base_controller import BaseController

from models.product_suppliers import ProductSupplier
from models.order_items import OrderItem
from models.categories import Category
from models.discounts import Discount
from models.shippings import Shipping
from models.suppliers import Supplier
from models.payments import Payment
from models.products import Product
from models.reviews import Review
from models.orders import Order
from models.users import User

from util.records import create_record_mapping
from util.validate_uuid import validate_uuid4


def create_user_object(user_data, many=False):
    users = [user.dump() for user in user_data] if many else [user_data.dump()]
    user_ids = tuple(set(user["user_id"] for user in users))

    reviews = []
    if user_ids:
        reviews_query = """SELECT * FROM "Reviews"
        WHERE customer_id IN %s"""
        cursor.execute(reviews_query, (user_ids,))
        reviews = Review.load_many(cursor.fetchall())
    user_reviews_mapping = create_record_mapping(reviews, key="customer_id", many=True)

    products = []
    if user_ids:
        review_product_ids = tuple(set(review.product_id for review in reviews))
        products_query = """SELECT * FROM "Products"
        WHERE created_by_id IN %s OR product_id IN %s"""
        cursor.execute(products_query, (user_ids, review_product_ids or user_ids))
        products = Product.load_many(cursor.fetchall())
    user_product_mapping = create_record_mapping(products, key="created_by_id", many=True)
    product_product_mapping = create_record_mapping(products)
    product_ids = tuple(set(product.product_id for product in products))

    categories = []
    if product_ids:
        categories_query = """SELECT "Categories".*, "ProductsCategoriesXref".product_id FROM "Categories"
        INNER JOIN "ProductsCategoriesXref" ON "ProductsCategoriesXref".category_id = "Categories".category_id
        WHERE "ProductsCategoriesXref".product_id IN %s"""
        cursor.execute(categories_query, (product_ids,))
        categories = Category.load_many(cursor.fetchall(), ["product_id"])
    product_category_mapping = create_record_mapping(categories, key="product_id", many=True)

    orders = []
    if user_ids:
        orders_query = """SELECT * FROM "Orders"
        WHERE customer_id IN %s"""
        cursor.execute(orders_query, (user_ids,))
        orders = Order.load_many(cursor.fetchall())
    user_order_mapping = create_record_mapping(orders, key="customer_id", many=True)
    order_ids = tuple(set(order.order_id for order in orders))

    shippings = []
    if order_ids:
        shippings_query = """SELECT * FROM "Shippings"
        WHERE order_id IN %s"""
        cursor.execute(shippings_query, (order_ids,))
        shippings = Shipping.load_many(cursor.fetchall())
    order_shipping_mapping = create_record_mapping(shippings, key="order_id")

    payments = []
    if order_ids:
        payments_query = """SELECT * FROM "Payments"
        WHERE order_id IN %s"""
        cursor.execute(payments_query, (order_ids,))
        payments = Payment.load_many(cursor.fetchall())
    order_payment_mapping = create_record_mapping(payments, key="order_id", many=True)

    discounts = []
    if order_ids:
        discounts_query = """SELECT "Discounts".*, "OrdersDiscountsXref".order_id FROM "Discounts"
        INNER JOIN "OrdersDiscountsXref" ON "OrdersDiscountsXref".discount_id = "Discounts".discount_id
        WHERE order_id IN %s"""
        cursor.execute(discounts_query, (order_ids,))
        discounts = Discount.load_many(cursor.fetchall(), ["order_id"])
    order_discounts_mapping = create_record_mapping(discounts, key="order_id", many=True)

    order_items = []
    if order_ids:
        order_items_query = """SELECT * FROM "OrderItems"
        WHERE order_id IN %s"""
        cursor.execute(order_items_query, (order_ids,))
        order_items = OrderItem.load_many(cursor.fetchall())
    order_order_items_mapping = create_record_mapping(order_items, key="order_id", many=True)

    product_suppliers = []
    if product_ids:
        product_supplier_query = """SELECT * FROM "ProductSuppliers"
        WHERE product_id IN %s"""
        cursor.execute(product_supplier_query, (product_ids,))
        product_suppliers = ProductSupplier.load_many(cursor.fetchall())
    supplier_product_supplier_mapping = create_record_mapping(product_suppliers, key="product_id", many=True)

    supplier_ids = set()
    for product_suppliers in supplier_product_supplier_mapping.values():
        supplier_ids.update(product_supplier["supplier_id"] for product_supplier in product_suppliers)

    if supplier_ids:
        suppliers_query = """SELECT * FROM "Suppliers"
        WHERE supplier_id IN %s"""
        cursor.execute(suppliers_query, (tuple(supplier_ids),))
        suppliers = Supplier.load_many(cursor.fetchall())
        supplier_product_mapping = create_record_mapping(suppliers)


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
    model = User

    def get_nested_records(self, record_id):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400

        get_by_id_query = f"""SELECT * FROM "{self.model.tablename}"
        WHERE {self.model.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()

        if not record:
            return jsonify({"message": "record not found"}), 404

        record = self.model().load(record)

        return jsonify({"message": "record found", "results": create_user_object(record)}), 200

    def get_all_nested_records(self):
        get_all_query = f'SELECT * FROM "{self.model.tablename}"'
        cursor.execute(get_all_query)

        records = self.model.load_many(cursor.fetchall())
        records = create_user_object(records, many=True)

        return jsonify({"message": "records found", "results": records}), 200
