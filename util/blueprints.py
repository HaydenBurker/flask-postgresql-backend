
from routes.users_routes import users
from routes.products_routes import products

def register_blueprints(app):
    app.register_blueprint(users)
    app.register_blueprint(products)
