from .base_routes import BaseRoutes
from controllers.reviews_controller import ReviewsController

reviews_routes = BaseRoutes("review", ReviewsController())
