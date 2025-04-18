from db import cursor

from .base_controller import BaseController
from models.order_items import base_order_item_object
from models.orders import base_order_object
from models.products import base_product_object
from util.records import create_record_mapping

def create_order_item_object(order_item_data, many=False):
    order_items = [base_order_item_object(o) for o in order_item_data] if many else [base_order_item_object(order_item_data)]
    order_ids = tuple(set(order["order_id"] for order in order_items))
    product_ids = tuple(set(order["product_id"] for order in order_items))

    if order_items:
        orders_query = """SELECT * FROM "Orders"
        WHERE order_id in %s"""
        cursor.execute(orders_query, (order_ids,))
        orders = cursor.fetchall()
        order_item_order_mapping = create_record_mapping(orders, base_order_object, key="order_id")

        products_query = """SELECT * FROM "Products"
        WHERE product_id in %s"""
        cursor.execute(products_query, (product_ids,))
        products = cursor.fetchall()
        order_item_product_mapping = create_record_mapping(products, base_product_object, key="product_id")

        for i, order_item in enumerate(order_items):
            order_items[i]["orders"] = order_item_order_mapping.get(order_item["order_id"])
            order_items[i]["products"] = order_item_product_mapping.get(order_item["product_id"])
            del order_items[i]["order_id"]
            del order_items[i]["product_id"]

    return order_items if many else order_items[0]

class OrderItemsController(BaseController):
    table_name = "OrderItems"
    post_data_fields = ["order_id", "product_id", "quantity", "unit_price"]
    default_values = [None, None, 0, 0]
    return_fields = ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "total_price"]
    create_record_object = lambda _, order_item, many=False: create_order_item_object(order_item, many)
