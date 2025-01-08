import uuid
from flask import request, jsonify

from db import connection, cursor

def add_record(table_name, post_data_fields, return_fields, create_record_object):
    post_data = request.json

    insert_query = f"""INSERT INTO "{table_name}"
    VALUES (%s,{",".join(["%s" for _ in post_data_fields])}) RETURNING {",".join(return_fields)}"""
    try:
        cursor.execute(insert_query, (str(uuid.uuid4()), *[post_data.get(field) for field in post_data_fields]))
        record = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to add record"}), 400

    return jsonify({"message": "added record", "results": create_record_object(record)}), 201
