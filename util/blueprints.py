
from routes.users_routes import users_routes
from routes.products_routes import products_routes
from routes.categories_routes import categories_routes
from routes.orders_routes import orders_routes
from routes.shippings_routes import shippings_routes
from routes.discounts_routes import discounts_routes
from routes.order_items_routes import order_items_routes
from routes.reviews_routes import reviews_routes
from routes.suppliers_routes import suppliers_routes

def register_blueprints(app):
    app.register_blueprint(users_routes.blueprint)
    app.register_blueprint(products_routes.blueprint)
    app.register_blueprint(categories_routes.blueprint)
    app.register_blueprint(orders_routes.blueprint)
    app.register_blueprint(shippings_routes.blueprint)
    app.register_blueprint(discounts_routes.blueprint)
    app.register_blueprint(order_items_routes.blueprint)
    app.register_blueprint(reviews_routes.blueprint)
    app.register_blueprint(suppliers_routes.blueprint)
