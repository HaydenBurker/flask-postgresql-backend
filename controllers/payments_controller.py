from .base_controller import BaseController
from models.payments import Payment


class PaymentsController(BaseController):
    model = Payment
