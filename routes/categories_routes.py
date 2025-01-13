from flask import Blueprint

from controllers.categories_controller import CategoriesController

categories = Blueprint("categories", __name__)
categories_controller = CategoriesController()

@categories.route("/category", methods=["POST"])
def add_category():
    return categories_controller.add_record()

@categories.route("/categories", methods=["GET"])
def get_all_categories():
    return categories_controller.get_all_records()

@categories.route("/category/<category_id>", methods=["GET"])
def get_category_by_id(category_id):
    return categories_controller.get_record_by_id(category_id)

@categories.route("/category/<category_id>", methods=["PUT"])
def update_category(category_id):
    return categories_controller.update_record(category_id)

@categories.route("/category/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    return categories_controller.delete_record(category_id)
