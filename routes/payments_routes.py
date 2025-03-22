from .base_routes import BaseRoutes
from controllers.payments_controller import PaymentsController

payments_routes = BaseRoutes("payment", PaymentsController())
