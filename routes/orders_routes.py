from .base_routes import BaseRoutes
from controllers.orders_controller import OrdersController

orders_routes = BaseRoutes("order", OrdersController())
orders_routes.blueprint.add_url_rule("/order/<record_id>", methods=["PATCH"], view_func=orders_routes.controller.record_activity)
