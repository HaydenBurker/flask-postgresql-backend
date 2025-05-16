from .base_controller import BaseController
from models.payments import base_payment_object


class PaymentsController(BaseController):
    table_name = "Payments"
    post_data_fields = ["order_id", "payment_method", "payment_date", "payment_status", "payment_amount"]
    default_values = [None, "", None, "", 0]
    return_fields = ["payment_id", "order_id", "payment_method", "payment_date", "payment_status", "payment_amount"]
    create_record_object = lambda _, payment_data, many=False: [base_payment_object(payment) for payment in payment_data] if many else base_payment_object(payment_data)
