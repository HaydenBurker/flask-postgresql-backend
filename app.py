from flask import Flask

import models.users
from routes.users_routes import users

app = Flask(__name__)

app.register_blueprint(users)

if __name__ == "__main__":
    app.run(port="8086", debug=True)
