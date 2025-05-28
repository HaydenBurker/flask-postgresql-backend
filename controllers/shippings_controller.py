from .base_controller import BaseController
from models.shippings import Shipping, base_shipping_object
from util.datetime import datetime_now

class ShippingsController(BaseController):
    create_record_object = lambda _, shipping_data, many=False: [base_shipping_object(shipping) for shipping in shipping_data] if many else base_shipping_object(shipping_data)
    model = Shipping
