import uuid
from flask import request, jsonify

from db import connection, cursor
from models.users import base_user_object
from models.products import base_product_object
from util.validate_uuid import validate_uuid4

table_name = "Users"

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
    post_data = request.json

    insert_query = f"""INSERT INTO "{table_name}" (user_id, first_name, last_name, email, password, active)
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id, first_name, last_name, email, active"""

    try:
        cursor.execute(insert_query, (str(uuid.uuid4()), post_data.get("first_name"), post_data.get("last_name"), post_data.get("email"), post_data.get("password"), post_data.get("active")))
        user = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to add user"}), 400

    return jsonify({"message": "added user", "results": create_user_object(user)}), 201

def get_all_users():
    get_all_query = f'SELECT user_id, first_name, last_name, email, active FROM "{table_name}"'
    cursor.execute(get_all_query)

    users = cursor.fetchall()
    users = [create_user_object(user) for user in users]

    return jsonify({"message": "users found", "results": users}), 200

def get_user_by_id(user_id):
    if not validate_uuid4(user_id):
        return jsonify({"message": "invalid user id"}), 400
    get_by_id_query = f"""SELECT user_id, first_name, last_name, email, active FROM "{table_name}"
    WHERE user_id = %s"""
    cursor.execute(get_by_id_query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "user not found"}), 404

    return jsonify({"message": "user found", "results": create_user_object(user)}), 200

def update_user(user_id):
    if not validate_uuid4(user_id):
        return jsonify({"message": "invalid user id"}), 400
    post_data = request.json
    get_by_id_query = f"""SELECT * FROM "{table_name}"
    WHERE user_id = %s"""
    cursor.execute(get_by_id_query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "user not found"}), 404

    [user_id, first_name, last_name, email, password, active] = user

    update_query = f"""UPDATE "{table_name}"
    SET first_name = %s,
    last_name = %s,
    email = %s,
    password = %s
    WHERE user_id = %s RETURNING user_id, first_name, last_name, email, active"""

    try:
        cursor.execute(update_query, (post_data.get("first_name") or first_name, post_data.get("last_name") or last_name, post_data.get("email") or email, post_data.get("password") or password, user_id))
        user = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to update user"}), 400
    return jsonify({"message": "user updated", "results": create_user_object(user)}), 200

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
