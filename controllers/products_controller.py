import uuid
from flask import request, jsonify

from db import connection, cursor
from models.products import create_product_object

def add_product():
    post_data = request.json

    insert_query = """INSERT INTO "Products"
    VALUES (%s, %s, %s) RETURNING *"""
    try:
        cursor.execute(insert_query, (str(uuid.uuid4()), post_data.get("name"), post_data.get("created_by_id")))
        product = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to add product"}), 400

    return jsonify({"message": "product added", "results": create_product_object(product)}), 201

def get_all_products():
    get_all_query = 'SELECT * FROM "Products"'
    cursor.execute(get_all_query)
    products = cursor.fetchall()

    products = [create_product_object(product) for product in products]

    return jsonify({"message": "products found", "results": products}), 200

def get_product_by_id(product_id):
    get_by_id_query = """SELECT * FROM "Products"
    WHERE product_id = %s"""
    cursor.execute(get_by_id_query, (product_id,))
    product = cursor.fetchone()
    if not product:
        return jsonify({"message": "product not found"}), 404

    return jsonify({"message": "product found", "results": create_product_object(product)}), 200

def update_product(product_id):
    post_data = request.json

    get_by_id_query = """SELECT * FROM "Products"
    WHERE product_id = %s"""
    cursor.execute(get_by_id_query, (product_id,))
    product = cursor.fetchone()
    if not product:
        return jsonify({"message": "product not found"}), 404

    [product_id, name, created_by_id] = product

    update_query = """UPDATE "Products"
    SET name = %s,
    created_by_id = %s
    WHERE product_id = %s RETURNING *"""
    try:
        cursor.execute(update_query, (post_data.get("name", name), post_data.get("created_by_id", created_by_id), product_id))
        product = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to update product"}), 400

    return jsonify({"message": "product updated", "results": create_product_object(product)}), 200

def delete_product(product_id):
    get_by_id_query = """SELECT product_id FROM "Products"
    WHERE product_id = %s"""
    cursor.execute(get_by_id_query, (product_id,))
    product = cursor.fetchone()
    if not product:
        return jsonify({"message": "product not found"}), 404

    [product_id] = product

    delete_query = """DELETE FROM "Products"
    WHERE product_id = %s"""
    try:
        cursor.execute(delete_query, (product_id,))
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to delete product"}), 400

    return jsonify({"message": "deleted product"}), 200

def product_add_category():
    post_data = request.json
    if "product_id" not in post_data or "category_id" not in post_data:
        return jsonify({"message": "product_id and category_id are required"}), 400
    product_id = post_data.get("product_id")
    category_id = post_data.get("category_id")

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

    return jsonify({"message": "category added to product", "results": create_product_object(product)})
