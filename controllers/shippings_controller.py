from .base_controller import BaseController
from models.shippings import base_shipping_object

class ShippingsController(BaseController):
    table_name = "Shippings"
    post_data_fields = ["order_id", "shipping_address", "shipping_label", "shipping_cost", "tracking_number", "shipping_status", "shipped_date"]
    default_values = [None, "", "", 0, "", "", None]
    return_fields = ["shipping_id", "order_id", "shipping_address", "shipping_label", "shipping_cost", "tracking_number", "shipping_status", "shipped_date"]
    create_record_object = lambda _, shipping: base_shipping_object(shipping)
