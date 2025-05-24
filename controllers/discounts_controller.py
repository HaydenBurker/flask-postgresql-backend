from .base_controller import BaseController
from models.discounts import Discount, base_discount_object

class DiscountsController(BaseController):
    table_name = "Discounts"
    post_data_fields = ["discount_code", "discount_type", "discount_value", "start_date", "end_date", "min_order_amount"]
    default_values = ["", "", 0, None, None, 0]
    return_fields = ["discount_id", "discount_code", "discount_type", "discount_value", "start_date", "end_date", "min_order_amount"]
    create_record_object = lambda _, discount_data, many=False: [base_discount_object(discount) for discount in discount_data] if many else base_discount_object(discount_data)
    model = Discount
