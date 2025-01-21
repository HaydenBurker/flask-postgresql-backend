from db import cursor

from .base_controller import BaseController
from models.order_items import base_order_item_object
from models.orders import base_order_object
from models.products import base_product_object

def create_order_item_object(order_item):
    order_item = base_order_item_object(order_item)
    order_id = order_item.get("order_id")
    product_id = order_item.get("product_id")

    order_query = """SELECT * FROM "Orders"
    WHERE order_id = %s"""
    cursor.execute(order_query, (order_id,))
    order = cursor.fetchone()
    order = base_order_object(order)
    order_item["order"] = order
    del order_item["order_id"]

    product_query = """SELECT * FROM "Products"
    WHERE product_id = %s"""
    cursor.execute(product_query, (product_id,))
    product = cursor.fetchone()
    product = base_product_object(product)
    order_item["product"] = product
    del order_item["product_id"]

    return order_item

class OrderItemsController(BaseController):
    table_name = "OrderItems"
    post_data_fields = ["order_id", "product_id", "quantity", "unit_price"]
    default_values = [None, None, 0, 0]
    return_fields = ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "total_price"]
    create_record_object = lambda _, order_item: create_order_item_object(order_item)
