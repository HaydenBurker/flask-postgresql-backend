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
    }})
