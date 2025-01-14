
from routes.users_routes import users_routes
from routes.products_routes import products_routes
from routes.categories_routes import categories_routes

def register_blueprints(app):
    app.register_blueprint(users_routes.blueprint)
    app.register_blueprint(products_routes.blueprint)
    app.register_blueprint(categories_routes.blueprint)
