from flask import Blueprint

from controllers import users_controller

users = Blueprint("users", __name__)

@users.route("/user", methods=["POST"])
def add_user():
    return users_controller.add_user()

@users.route("/users", methods=["GET"])
def get_all_users():
    return users_controller.get_all_users()

@users.route("/user/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    return users_controller.get_user_by_id(user_id)

@users.route("/user/<user_id>", methods=["PUT"])
def update_user(user_id):
    return users_controller.update_user(user_id)

@users.route("/user/<user_id>", methods=["PATCH"])
def user_activity(user_id):
    return users_controller.user_activity(user_id)

@users.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    return users_controller.delete_user(user_id)
