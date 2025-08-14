from .base_controller import BaseController
from models.shippings import Shipping


class ShippingsController(BaseController):
    model = Shipping
