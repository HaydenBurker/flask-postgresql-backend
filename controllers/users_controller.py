import uuid
from flask import request, jsonify

from db import get_connection

def add_user():
    post_data = request.json
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """INSERT INTO "Users" (user_id, first_name, last_name, email, password, active)
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING *"""

    cursor.execute(insert_query, (str(uuid.uuid4()), post_data.get("first_name"), post_data.get("last_name"), post_data.get("email"), post_data.get("password"), post_data.get("active")))
    [user_id, first_name, last_name, email, password, active] = cursor.fetchone()
    connection.commit()

    return jsonify({"message": "added user", "results": {
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "active": active
    }}), 201

def get_all_users():
    connection = get_connection()
    cursor = connection.cursor()

    get_all_query = 'SELECT user_id, first_name, last_name, email, active FROM "Users"'
    cursor.execute(get_all_query)

    users = cursor.fetchall()

    users = [{"user_id": user_id, "first_name": first_name, "last_name": last_name, "email": email, "active": active} for [user_id, first_name, last_name, email, active] in users]

    return jsonify({"message": "users found", "results": users}), 200

def get_user_by_id(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    get_by_id_query = """SELECT user_id, first_name, last_name, email, active FROM "Users"
    WHERE user_id = %s"""
    cursor.execute(get_by_id_query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "user not found"}), 404

    [user_id, first_name, last_name, email, active] = user
    user = {"user_id": user_id, "first_name": first_name, "last_name": last_name, "email": email, "active": active}
    return jsonify({"message": "user found", "results": user}), 200

def update_user(user_id):
    post_data = request.json
    connection = get_connection()
    cursor = connection.cursor()

    get_by_id_query = """SELECT * FROM "Users"
    WHERE user_id = %s"""
    cursor.execute(get_by_id_query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "user not found"}), 404

    [user_id, first_name, last_name, email, password, active] = user

    update_query = """UPDATE "Users"
    SET first_name = %s,
    last_name = %s,
    email = %s,
    password = %s
    WHERE user_id = %s RETURNING *"""
    cursor.execute(update_query, (post_data.get("first_name") or first_name, post_data.get("last_name") or last_name, post_data.get("email") or email, post_data.get("password") or password, user_id))
    user = cursor.fetchone()
    connection.commit()

    [user_id, first_name, last_name, email, password, active] = user
    user = {"user_id": user_id, "first_name": first_name, "last_name": last_name, "email": email, "active": active}
    return jsonify({"message": "user updated", "results": user}), 200

def user_activity(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    get_by_id_query = """SELECT active FROM "Users"
    WHERE user_id = %s"""
    cursor.execute(get_by_id_query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "user not found"}), 404

    [active] = user

    activity_query = """UPDATE "Users"
    SET active = %s
    WHERE user_id = %s RETURNING *"""
    cursor.execute(activity_query, (not active, user_id))
    user = cursor.fetchone()
    connection.commit()

    [user_id, first_name, last_name, email, password, active] = user
    user = {"user_id": user_id, "first_name": first_name, "last_name": last_name, "email": email, "active": active}
    return jsonify({"message": f"user {'activated' if active else 'deactivated'}", "results": user}), 200

def delete_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    get_by_id_query = """SELECT user_id FROM "Users"
    WHERE user_id = %s"""
    cursor.execute(get_by_id_query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "user not found"}), 404

    [user_id] = user

    delete_query = """DELETE FROM "Users"
    WHERE user_id = %s"""
    cursor.execute(delete_query, (user_id,))
    connection.commit()

    return jsonify({"message": "user deleted"}), 200
