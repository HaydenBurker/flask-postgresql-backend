
from routes.users_routes import users

def register_blueprints(app):
    app.register_blueprint(users)
