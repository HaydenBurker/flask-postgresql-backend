from flask import request, jsonify

from db import connection, cursor
from .base_controller import add_record, get_all_records
from models.categories import base_category_object
from util.validate_uuid import validate_uuid4

table_name = "Categories"
post_data_fields = ["name"]
return_fields = ["category_id", "name"]

def add_category():
    return add_record(table_name, post_data_fields, return_fields, base_category_object)

def get_all_categories():
    return get_all_records(table_name, return_fields, base_category_object)

def get_category_by_id(category_id):
    if not validate_uuid4(category_id):
        return jsonify({"message": "invalid category id"}), 400
    get_by_id_query = f"""SELECT * FROM "{table_name}"
    WHERE category_id = %s"""
    cursor.execute(get_by_id_query, (category_id,))
    category = cursor.fetchone()
    if not category:
        return jsonify({"message": "category not found"}), 404

    return jsonify({"message": "category found", "results": base_category_object(category)}), 200

def update_category(category_id):
    if not validate_uuid4(category_id):
        return jsonify({"message": "invalid category id"}), 400
    post_data = request.json

    get_by_id_query = f"""SELECT * FROM "{table_name}"
    WHERE category_id = %s"""
    cursor.execute(get_by_id_query, (category_id,))
    category = cursor.fetchone()
    if not category:
        return jsonify({"message": "category not found"}), 404

    [category_id, name] = category

    update_query = f"""UPDATE "{table_name}"
    SET name = %s
    WHERE category_id = %s RETURNING *"""
    try:
        cursor.execute(update_query, (post_data.get("name", name), category_id))
        category = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to update category"}), 400

    return jsonify({"message": "category updated", "results": base_category_object(category)}), 200

def delete_category(category_id):
    if not validate_uuid4(category_id):
        return jsonify({"message": "invalid category id"}), 400
    get_by_id_query = f"""SELECT category_id FROM "{table_name}"
    WHERE category_id = %s"""
    cursor.execute(get_by_id_query, (category_id,))
    category = cursor.fetchone()
    if not category:
        return jsonify({"message": "category not found"}), 404

    [category_id] = category

    delete_query = f"""DELETE FROM "{table_name}"
    WHERE category_id = %s"""
    try:
        cursor.execute(delete_query, (category_id,))
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to delete category"}), 400

    return jsonify({"message": "deleted category"}), 200
