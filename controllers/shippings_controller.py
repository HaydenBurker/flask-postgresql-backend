from .base_controller import BaseController
from models.shippings import Shipping

class ShippingsController(BaseController):
    create_record_object = lambda _, shipping_data, many=False: [shipping.dump() for shipping in shipping_data] if many else shipping_data.dump()
    model = Shipping
