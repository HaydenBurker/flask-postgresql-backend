from .base_routes import BaseRoutes
from controllers.order_items_controller import OrderItemsController

order_items_routes = BaseRoutes("order-item", OrderItemsController())
