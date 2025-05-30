from .base_controller import BaseController
from models.discounts import Discount

class DiscountsController(BaseController):
    create_record_object = lambda _, discount_data, many=False: [discount.dump() for discount in discount_data] if many else discount_data.dump()
    model = Discount
