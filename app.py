from flask import Flask

from util.blueprints import register_blueprints
from middleware import ExceptionHandlerMiddleware

app = Flask(__name__)

# app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)

register_blueprints(app)

if __name__ == "__main__":
    app.run(port="8086", debug=True)
