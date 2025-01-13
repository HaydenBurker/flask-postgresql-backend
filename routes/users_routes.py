from flask import Blueprint

from controllers.users_controller import UsersController

users = Blueprint("users", __name__)
users_controller = UsersController()

@users.route("/user", methods=["POST"])
def add_user():
    return users_controller.add_record()

@users.route("/users", methods=["GET"])
def get_all_users():
    return users_controller.get_all_records()

@users.route("/user/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    return users_controller.get_record_by_id(user_id)

@users.route("/user/<user_id>", methods=["PUT"])
def update_user(user_id):
    return users_controller.update_record(user_id)

@users.route("/user/<user_id>", methods=["PATCH"])
def user_activity(user_id):
    return users_controller.record_activity(user_id)

@users.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    return users_controller.delete_record(user_id)
