from .base_routes import BaseRoutes
from controllers.categories_controller import CategoriesController

categories_routes = BaseRoutes("category", CategoriesController())
