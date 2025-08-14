from .base_controller import BaseController
from models.discounts import Discount


class DiscountsController(BaseController):
    model = Discount
