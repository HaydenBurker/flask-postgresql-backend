import uuid
from flask import request, jsonify

from db import connection, cursor
from models.categories import create_category_object

def add_category():
    post_data = request.json

    insert_query = """INSERT INTO "Categories"
    VALUES (%s, %s) RETURNING *"""
    try:
        cursor.execute(insert_query, (str(uuid.uuid4()), post_data.get("name")))
        category = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to add category"}), 400

    return jsonify({"message": "category added", "results": create_category_object(category)}), 201

def get_all_categories():
    get_all_query = 'SELECT * FROM "Categories"'
    cursor.execute(get_all_query)
    categories = cursor.fetchall()

    categories = [create_category_object(category) for category in categories]

    return jsonify({"message": "categories found", "results": categories}), 200

def get_category_by_id(category_id):
    get_by_id_query = """SELECT * FROM "Categories"
    WHERE category_id = %s"""
    cursor.execute(get_by_id_query, (category_id,))
    category = cursor.fetchone()
    if not category:
        return jsonify({"message": "category not found"}), 404

    return jsonify({"message": "category found", "results": create_category_object(category)}), 200

def update_category(category_id):
    post_data = request.json

    get_by_id_query = """SELECT * FROM "Categories"
    WHERE category_id = %s"""
    cursor.execute(get_by_id_query, (category_id,))
    category = cursor.fetchone()
    if not category:
        return jsonify({"message": "category not found"}), 404

    [category_id, name] = category

    update_query = """UPDATE "Categories"
    SET name = %s
    WHERE category_id = %s RETURNING *"""
    try:
        cursor.execute(update_query, (post_data.get("name", name), category_id))
        category = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to update category"}), 400

    return jsonify({"message": "category updated", "results": create_category_object(category)}), 200

def delete_category(category_id):
    get_by_id_query = """SELECT category_id FROM "Categories"
    WHERE category_id = %s"""
    cursor.execute(get_by_id_query, (category_id,))
    category = cursor.fetchone()
    if not category:
        return jsonify({"message": "category not found"}), 404

    [category_id] = category

    delete_query = """DELETE FROM "Categories"
    WHERE category_id = %s"""
    try:
        cursor.execute(delete_query, (category_id,))
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to delete category"}), 400

    return jsonify({"message": "deleted category"}), 200
