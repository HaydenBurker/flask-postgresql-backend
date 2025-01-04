from flask import Blueprint

from controllers import categories_controller

categories = Blueprint("categories", __name__)

@categories.route("/category", methods=["POST"])
def add_category():
    return categories_controller.add_category()

@categories.route("/categories", methods=["GET"])
def get_all_categories():
    return categories_controller.get_all_categories()

@categories.route("/category/<category_id>", methods=["GET"])
def get_category_by_id(category_id):
    return categories_controller.get_category_by_id(category_id)

@categories.route("/category/<category_id>", methods=["PUT"])
def update_category(category_id):
    return categories_controller.update_category(category_id)

@categories.route("/category/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    return categories_controller.delete_category(category_id)
