from .base_controller import BaseController
from models.shippings import base_shipping_object
from util.datetime import datetime_now

class ShippingsController(BaseController):
    table_name = "Shippings"
    post_data_fields = ["order_id", "shipping_address", "shipping_label", "shipping_cost", "tracking_number", "shipping_status", "shipped_date"]
    default_values = [None, "", "", 0, "", "", datetime_now]
    return_fields = ["shipping_id", "order_id", "shipping_address", "shipping_label", "shipping_cost", "tracking_number", "shipping_status", "shipped_date"]
    create_record_object = lambda _, shipping_data, many=False: [base_shipping_object(shipping) for shipping in shipping_data] if many else base_shipping_object(shipping_data)
