from db import cursor
from .base_controller import BaseController
from models.orders import base_order_object
from models.users import base_user_object


def create_order_object(order):
    order = base_order_object(order)
    customer_id = order.get("customer_id")

    create_by_id_query = """SELECT user_id, first_name, last_name, email, active, created_at, updated_at FROM "Users"
    WHERE user_id = %s"""
    cursor.execute(create_by_id_query, (customer_id,))
    user = cursor.fetchone()
    customer = base_user_object(user)

    del order["customer_id"]
    order["customer"] = customer
    return order

class OrdersController(BaseController):
    table_name = "Orders"
    post_data_fields = ["customer_id", "shipping_date", "status", "total_amount", "active"]
    default_values = [None, None, "", 0, True, None, None]
    return_fields = ["order_id", "customer_id", "shipping_date", "status", "total_amount", "active", "created_at", "updated_at"]
    create_record_object = lambda _, order: create_order_object(order)
