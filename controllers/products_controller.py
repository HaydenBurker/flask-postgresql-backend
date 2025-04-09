from flask import request, jsonify

from db import connection, cursor
from .base_controller import BaseController
from models.products import base_product_object
from models.categories import base_category_object
from models.users import base_user_object
from util.validate_uuid import validate_uuid4
from util.records import create_record_mapping


def create_product_object(product_data, many=False):
    products = [base_product_object(product) for product in product_data] if many else [base_product_object(product_data)]
    product_ids = tuple(product["product_id"] for product in products)
    created_by_ids = tuple(product["created_by_id"] for product in products)

    users = []
    if created_by_ids:
        users_query = """SELECT user_id, first_name, last_name, email, active, created_at, updated_at FROM "Users"
        WHERE user_id IN %s"""
        cursor.execute(users_query, (created_by_ids,))
        users = cursor.fetchall()
    product_user_mapping = create_record_mapping(users, base_user_object, key="user_id")

    categories = []
    if product_ids:
        categories_query = """SELECT "Categories".category_id, "Categories".name, "Categories".description, "ProductsCategoriesXref".product_id FROM "Categories"
        INNER JOIN "ProductsCategoriesXref" ON "ProductsCategoriesXref".category_id = "Categories".category_id
        WHERE "ProductsCategoriesXref".product_id IN %s"""
        cursor.execute(categories_query, (product_ids,))
        categories = cursor.fetchall()
    product_category_mapping = create_record_mapping(categories, base_category_object, many=True)

    ratings = []
    if product_ids:
        ratings_query = """SELECT AVG(rating), product_id FROM "Reviews"
        WHERE product_id in %s
        GROUP BY product_id"""
        cursor.execute(ratings_query, (product_ids,))
        ratings = cursor.fetchall()
    product_rating_mapping = create_record_mapping(ratings, lambda record: record[0])

    for i, product in enumerate(products):
        product_id = product["product_id"]
        products[i]["created_by_user"] = product_user_mapping.get(product["created_by_id"])
        products[i]["categories"] = product_category_mapping.get(product_id, [])
        products[i]["rating"] = product_rating_mapping.get(product_id)
        del products[i]["created_by_id"]

    return products if many else products[0]

class ProductsController(BaseController):
    table_name = "Products"
    post_data_fields = ["name", "description", "price", "stock_quantity", "created_by_id"]
    default_values = ["", "", 0, 0, None, None, None]
    return_fields = ["product_id", "name", "description", "price", "stock_quantity", "created_by_id", "created_at", "updated_at"]
    create_record_object = lambda _, product, many=False: create_product_object(product, many)

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
