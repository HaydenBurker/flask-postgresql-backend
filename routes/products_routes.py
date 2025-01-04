from flask import Blueprint

from controllers import products_controller

products = Blueprint("products", __name__)

@products.route("/product", methods=["POST"])
def add_product():
    return products_controller.add_product()

@products.route("/products", methods=["GET"])
def get_all_products():
    return products_controller.get_all_products()
