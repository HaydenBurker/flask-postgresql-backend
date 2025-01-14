from .base_routes import BaseRoutes
from controllers.products_controller import ProductsController

products_routes = BaseRoutes("product", ProductsController())

@products_routes.blueprint.route("/product/add-category", methods=["PATCH"])
def product_add_category():
    return products_routes.controller.product_add_category()
