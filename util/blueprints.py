
from routes.users_routes import users
from routes.products_routes import products
from routes.categories_routes import categories

def register_blueprints(app):
    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(categories)
