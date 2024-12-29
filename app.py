from flask import Flask

from util.blueprints import register_blueprints

app = Flask(__name__)

register_blueprints(app)

if __name__ == "__main__":
    app.run(port="8086", debug=True)
