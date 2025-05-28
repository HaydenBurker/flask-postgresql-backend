from .base_controller import BaseController
from models.discounts import Discount, base_discount_object

class DiscountsController(BaseController):
    create_record_object = lambda _, discount_data, many=False: [base_discount_object(discount) for discount in discount_data] if many else base_discount_object(discount_data)
    model = Discount
