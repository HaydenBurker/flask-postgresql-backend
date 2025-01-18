from flask import request, jsonify

from db import connection, cursor
from .base_controller import BaseController
from models.products import base_product_object
from models.categories import base_category_object
from models.users import base_user_object
from util.validate_uuid import validate_uuid4


def create_product_object(product):
    product = base_product_object(product)
    product_id = product.get("product_id")
    created_by_id = product.get("created_by_id")
    created_by_user = created_by_id
    categories = []

    if created_by_id:
        create_by_id_query = """SELECT user_id, first_name, last_name, email, active, created_at, updated_at FROM "Users"
        WHERE user_id = %s"""
        cursor.execute(create_by_id_query, (created_by_id,))
        user = cursor.fetchone()
        created_by_user = base_user_object(user)

    categories_query = """SELECT "Categories".category_id, "Categories".name, "Categories".description FROM "Categories"
    INNER JOIN "ProductsCategoriesXref" ON "ProductsCategoriesXref".category_id = "Categories".category_id
    WHERE "ProductsCategoriesXref".product_id = %s"""
    cursor.execute(categories_query, (product_id,))
    categories = cursor.fetchall()
    categories = [base_category_object(category) for category in categories]

    del product["created_by_id"]
    product["created_by"] = created_by_user
    product["categories"] = categories
    return product

class ProductsController(BaseController):
    table_name = "Products"
    post_data_fields = ["name", "description", "price", "stock_quantity", "created_by_id"]
    default_values = ["", "", 0, 0, None, None, None]
    return_fields = ["product_id", "name", "description", "price", "stock_quantity", "created_by_id", "created_at", "updated_at"]
    create_record_object = lambda _, product: create_product_object(product)

    def product_add_category(self):
        post_data = request.json
        if "product_id" not in post_data or "category_id" not in post_data:
            return jsonify({"message": "product_id and category_id are required"}), 400
        product_id = post_data.get("product_id")
        category_id = post_data.get("category_id")

        if not validate_uuid4(product_id):
            return jsonify({"message": "invalid product id"}), 400

        if not validate_uuid4(category_id):
            return jsonify({"message": "invalid category id"}), 400

        product_query = """SELECT * FROM "Products"
        WHERE product_id = %s"""
        cursor.execute(product_query, (product_id,))
        product = cursor.fetchone()
        product_id = product[0]
        if not product_id:
            return jsonify({"message": "product not found"}), 404

        cateogy_query = """SELECT category_id FROM "Categories"
        WHERE category_id = %s"""
        cursor.execute(cateogy_query, (category_id,))
        [category_id] = cursor.fetchone()
        if not category_id:
            return jsonify({"message": "category not found"}), 404
        
        product_add_category_query = """INSERT INTO "ProductsCategoriesXref" (product_id, category_id)
        VALUES (%s, %s) RETURNING *"""
        try:
            cursor.execute(product_add_category_query, (product_id, category_id))
            [product_id, category_id] = cursor.fetchone()
            connection.commit()
        except:
            connection.rollback()
            return jsonify({"message": "cannot add category to product"}), 400

        return jsonify({"message": "category added to product", "results": create_product_object(product)}), 200
