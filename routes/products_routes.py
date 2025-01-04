from flask import Blueprint

from controllers import products_controller

products = Blueprint("products", __name__)

@products.route("/product", methods=["POST"])
def add_product():
    return products_controller.add_product()

@products.route("/products", methods=["GET"])
def get_all_products():
    return products_controller.get_all_products()

@products.route("/product/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    return products_controller.get_product_by_id(product_id)

@products.route("/product/<product_id>", methods=["PUT"])
def update_product(product_id):
    return products_controller.update_product(product_id)

@products.route("/product/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    return products_controller.delete_product(product_id)

@products.route("/product/add-category", methods=["PATCH"])
def product_add_category():
    return products_controller.product_add_category()
