from flask import request, jsonify

from db import connection, cursor
from .base_controller import add_record, get_all_records, get_record_by_id, update_record
from models.users import base_user_object
from models.products import base_product_object
from util.validate_uuid import validate_uuid4

table_name = "Users"
post_data_fields = ["first_name", "last_name", "email", "password", "active"]
return_fields = ["user_id", "first_name", "last_name", "email", "active"]

def create_user_object(user):
    user = base_user_object(user)
    user_id = user.get("user_id")
    products = []

    products_query = """SELECT * FROM "Products"
    WHERE created_by_id = %s"""
    cursor.execute(products_query, (user_id,))
    products = cursor.fetchall()
    products = [base_product_object(product) for product in products]

    user["products"] = products
    return user

def add_user():
    return add_record(table_name, post_data_fields, return_fields, create_user_object)

def get_all_users():
    return get_all_records(table_name, return_fields, create_user_object)

def get_user_by_id(user_id):
    return get_record_by_id(user_id, table_name, return_fields, create_user_object)

def update_user(user_id):
    return update_record(user_id, table_name, post_data_fields[:-1], return_fields, create_user_object)

def user_activity(user_id):
    if not validate_uuid4(user_id):
        return jsonify({"message": "invalid user id"}), 400
    get_by_id_query = f"""SELECT active FROM "{table_name}"
    WHERE user_id = %s"""
    cursor.execute(get_by_id_query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "user not found"}), 404

    [active] = user

    activity_query = f"""UPDATE "{table_name}"
    SET active = %s
    WHERE user_id = %s RETURNING user_id, first_name, last_name, email, active"""
    active = not active
    cursor.execute(activity_query, (active, user_id))
    user = cursor.fetchone()
    connection.commit()

    return jsonify({"message": f"user {'activated' if active else 'deactivated'}", "results": create_user_object(user)}), 200

def delete_user(user_id):
    if not validate_uuid4(user_id):
        return jsonify({"message": "invalid user id"}), 400
    get_by_id_query = f"""SELECT user_id FROM "{table_name}"
    WHERE user_id = %s"""
    cursor.execute(get_by_id_query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "user not found"}), 404

    [user_id] = user

    delete_query = f"""DELETE FROM "{table_name}"
    WHERE user_id = %s"""
    try:
        cursor.execute(delete_query, (user_id,))
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to delete user"}), 400

    return jsonify({"message": "user deleted"}), 200
