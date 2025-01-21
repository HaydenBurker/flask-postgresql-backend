from .base_routes import BaseRoutes
from controllers.suppliers_controller import SuppliersController

suppliers_routes = BaseRoutes("supplier", SuppliersController())
suppliers_routes.blueprint.add_url_rule("/supplier/add-product-supplier", methods=["PATCH"], view_func=suppliers_routes.controller.add_product_supplier)
