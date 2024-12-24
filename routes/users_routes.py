from flask import Blueprint

from controllers import users_controller

users = Blueprint("users", __name__)

@users.route("/user", methods=["POST"])
def add_user():
    return users_controller.add_user()
