from .base_routes import BaseRoutes
from controllers.users_controller import UsersController

users_routes = BaseRoutes("user", UsersController())
users_routes.blueprint.add_url_rule(f"/user/<record_id>", methods=["PATCH"], view_func=users_routes.controller.record_activity)
