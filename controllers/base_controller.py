import uuid
from flask import request, jsonify

from db import connection, cursor
from util.validate_uuid import validate_uuid4

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

def get_all_records(table_name, return_fields, create_record_object):
    get_all_query = f'SELECT {",".join(return_fields)} FROM "{table_name}"'
    cursor.execute(get_all_query)

    records = cursor.fetchall()
    records = [create_record_object(record) for record in records]

    return jsonify({"message": "records found", "results": records}), 200

def get_record_by_id(record_id, table_name, return_fields, create_record_object):
    if not validate_uuid4(record_id):
        return jsonify({"message": "invalid record id"}), 400
    get_by_id_query = f"""SELECT {",".join(return_fields)} FROM "{table_name}"
    WHERE {return_fields[0]} = %s"""
    cursor.execute(get_by_id_query, (record_id,))
    record = cursor.fetchone()
    if not record:
        return jsonify({"message": "record not found"}), 404

    return jsonify({"message": "record found", "results": create_record_object(record)}), 200

def update_record(record_id, table_name, post_data_fields, return_fields, create_record_object):
    if not validate_uuid4(record_id):
        return jsonify({"message": "invalid record id"}), 400
    post_data = request.json
    get_by_id_query = f"""SELECT {",".join(post_data_fields)} FROM "{table_name}"
    WHERE {return_fields[0]} = %s"""
    cursor.execute(get_by_id_query, (record_id,))
    record = cursor.fetchone()
    if not record:
        return jsonify({"message": "record not found"}), 404

    update_fields = ",".join(f"{field} = %s" for field in post_data_fields)

    update_query = f"""UPDATE "{table_name}"
    SET {update_fields}
    WHERE {return_fields[0]} = %s RETURNING {",".join(return_fields)}"""

    try:
        cursor.execute(update_query, (*[post_data.get(field, value) for (field, value) in zip(post_data_fields, record)], record_id))
        record = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to update record"}), 400
    return jsonify({"message": "record updated", "results": create_record_object(record)}), 200

def record_activity(record_id, table_name, return_fields, create_record_object, active_field="active"):
    if not validate_uuid4(record_id):
        return jsonify({"message": "invalid record id"}), 400
    get_by_id_query = f"""SELECT {active_field} FROM "{table_name}"
    WHERE {return_fields[0]} = %s"""
    cursor.execute(get_by_id_query, (record_id,))
    record = cursor.fetchone()
    if not record:
        return jsonify({"message": "record not found"}), 404

    [active] = record

    activity_query = f"""UPDATE "{table_name}"
    SET {active_field} = %s
    WHERE {return_fields[0]} = %s RETURNING {",".join(return_fields)}"""
    active = not active
    cursor.execute(activity_query, (active, record_id))
    record = cursor.fetchone()
    connection.commit()

    return jsonify({"message": f"record {'activated' if active else 'deactivated'}", "results": create_record_object(record)}), 200

def delete_record(record_id, table_name, primary_key):
    if not validate_uuid4(record_id):
        return jsonify({"message": "invalid record id"}), 400
    get_by_id_query = f"""SELECT {primary_key} FROM "{table_name}"
    WHERE {primary_key} = %s"""
    cursor.execute(get_by_id_query, (record_id,))
    record = cursor.fetchone()
    if not record:
        return jsonify({"message": "record not found"}), 404

    [record_id] = record

    delete_query = f"""DELETE FROM "{table_name}"
    WHERE {primary_key} = %s"""
    try:
        cursor.execute(delete_query, (record_id,))
        connection.commit()
    except:
        connection.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "record deleted"}), 200
