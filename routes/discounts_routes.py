from .base_routes import BaseRoutes
from controllers.discounts_controller import DiscountsController

discounts_routes = BaseRoutes("discount", DiscountsController())
