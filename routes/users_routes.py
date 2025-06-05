from .base_routes import BaseRoutes
from controllers.users_controller import UsersController

users_routes = BaseRoutes("user", UsersController())
users_routes.blueprint.add_url_rule(f"/user/<record_id>", methods=["PATCH"], view_func=users_routes.controller.record_activity)
users_routes.blueprint.add_url_rule(f"/user/nested/<record_id>", methods=["GET"], view_func=users_routes.controller.get_nested_records)
users_routes.blueprint.add_url_rule(f"/users/nested", methods=["GET"], view_func=users_routes.controller.get_all_nested_records)
