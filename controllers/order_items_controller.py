from db import cursor

from .base_controller import BaseController
from models.order_items import OrderItem
from models.orders import Order
from models.products import Product
from util.records import create_record_mapping

def create_order_item_object(order_item_data, many=False):
    order_items = [o.dump() for o in order_item_data] if many else [order_item_data.dump()]
    order_ids = tuple(set(order["order_id"] for order in order_items))
    product_ids = tuple(set(order["product_id"] for order in order_items))

    if order_items:
        orders_query = """SELECT * FROM "Orders"
        WHERE order_id in %s"""
        cursor.execute(orders_query, (order_ids,))
        orders = Order.load_many(cursor.fetchall())
        order_item_order_mapping = create_record_mapping(orders)

        products_query = """SELECT * FROM "Products"
        WHERE product_id in %s"""
        cursor.execute(products_query, (product_ids,))
        products = Product.load_many(cursor.fetchall())
        order_item_product_mapping = create_record_mapping(products)

        for i, order_item in enumerate(order_items):
            order_items[i]["order"] = order_item_order_mapping.get(order_item["order_id"])
            order_items[i]["product"] = order_item_product_mapping.get(order_item["product_id"])
            del order_items[i]["order_id"]
            del order_items[i]["product_id"]

    return order_items if many else order_items[0]

class OrderItemsController(BaseController):
    create_record_object = lambda _, order_item, many=False: create_order_item_object(order_item, many)
    model = OrderItem
