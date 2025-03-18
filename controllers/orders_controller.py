from flask import request, jsonify

from db import connection, cursor
from .base_controller import BaseController
from models.orders import base_order_object
from models.users import base_user_object
from models.discounts import base_discount_object
from util.validate_uuid import validate_uuid4
from util.records import create_record_mapping


def create_order_object(order_data, many=False):
    orders = [base_order_object(order) for order in order_data] if many else [base_order_object(order_data)]
    order_ids = tuple(order["order_id"] for order in orders)
    customer_ids = tuple(order["customer_id"] for order in orders)

    users_query = """SELECT user_id, first_name, last_name, email, active, created_at, updated_at FROM "Users"
    WHERE user_id IN %s"""
    cursor.execute(users_query, (customer_ids,))
    users = cursor.fetchall()

    order_user_mapping = create_record_mapping(users, base_user_object, key="user_id", many=False)

    discounts_query = """SELECT "Discounts".discount_id, "Discounts".discount_code, "Discounts".discount_type, "Discounts".discount_value, "Discounts".start_date, "Discounts".end_date, "Discounts".min_order_amount, "OrdersDiscountsXref".order_id FROM "Discounts"
    INNER JOIN "OrdersDiscountsXref" ON "OrdersDiscountsXref".discount_id = "Discounts".discount_id
    WHERE "OrdersDiscountsXref".order_id IN %s"""
    cursor.execute(discounts_query, (order_ids,))
    discounts = cursor.fetchall()

    order_discount_mapping = create_record_mapping(discounts, base_discount_object, many=True)

    for i, order in enumerate(orders):
        orders[i]["customer"] = order_user_mapping.get(order["customer_id"], [])
        orders[i]["discounts"] = order_discount_mapping.get(order["order_id"], [])
        del orders[i]["customer_id"]

    return orders if many else orders[0]

class OrdersController(BaseController):
    table_name = "Orders"
    post_data_fields = ["customer_id", "order_date", "shipping_date", "status", "total_amount", "active"]
    default_values = [None, None, None, "", 0, True, None, None]
    return_fields = ["order_id", "customer_id", "shipping_date", "status", "total_amount", "active", "created_at", "updated_at"]
    create_record_object = lambda _, order, many=False: create_order_object(order, many)

    def order_add_discount(self):
        post_data = request.json

        order_id = post_data.get("order_id")
        if not validate_uuid4(order_id):
            return jsonify({"message": "invalid order id"}), 400
        order_query = """SELECT * FROM "Orders"
        WHERE order_id = %s"""
        cursor.execute(order_query, (order_id,))
        order = cursor.fetchone()
        if not order:
            return jsonify({"message": "order not found"}), 404

        discount_id = post_data.get("discount_id")
        if not validate_uuid4(discount_id):
            return jsonify({"message": "invalid discount id"}), 400
        discount_query = """SELECT discount_id FROM "Discounts"
        WHERE discount_id = %s"""
        cursor.execute(discount_query, (discount_id,))
        discount = cursor.fetchone()
        [discount_id] = discount
        if not discount:
            return jsonify({"message": "discount not found"}), 404

        order_add_discount_query = """INSERT INTO "OrdersDiscountsXref" (order_id, discount_id)
        VALUES (%s, %s)"""
        try:
            cursor.execute(order_add_discount_query, (order_id, discount_id))
            connection.commit()
        except:
            connection.rollback()
            return jsonify({"message": "unable to add discount to order"}), 400

        return jsonify({"message": "discount added to order", "results": create_order_object(order)}), 200
