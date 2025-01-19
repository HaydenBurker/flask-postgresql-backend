from .base_routes import BaseRoutes
from controllers.shippings_controller import ShippingsController

shippings_routes = BaseRoutes("shipping", ShippingsController())
