from .base_controller import BaseController
from models.payments import Payment


class PaymentsController(BaseController):
    create_record_object = lambda _, payment_data, many=False: [payment.dump() for payment in payment_data] if many else payment_data.dump()
    model = Payment
