import uuid
import types
from flask import request, jsonify
from datetime import datetime, timezone

from db import connection, cursor
from util.validate_uuid import validate_uuid4
from util.datetime import datetime_now

class BaseController:
    table_name = None
    post_data_fields = []
    default_values = []
    return_fields = []
    create_record_object = None

    def __init__(self):
        self.primary_key = self.return_fields[0]

    def add_record(self):
        post_data = request.json
        insert_fields = self.post_data_fields.copy()
        current_datetime = datetime_now()

        if "created_at" in self.return_fields:
            insert_fields.append("created_at")
            post_data["created_at"] = current_datetime
        if "updated_at" in self.return_fields:
            insert_fields.append("updated_at")
            post_data["updated_at"] = current_datetime

        insert_query = f"""INSERT INTO "{self.table_name}"
        VALUES (%s,{",".join(["%s" for _ in insert_fields])}) RETURNING {",".join(self.return_fields)}"""
        try:
            cursor.execute(insert_query, (str(uuid.uuid4()), *[post_data.get(field, value() if isinstance(value, types.FunctionType) else value) for field, value in zip(insert_fields, self.default_values)]))
            record = cursor.fetchone()
            connection.commit()
        except:
            connection.rollback()
            return jsonify({"message": "unable to add record"}), 400

        return jsonify({"message": "added record", "results": self.create_record_object(record)}), 201

    def get_all_records(self):
        get_all_query = f'SELECT {",".join(self.return_fields)} FROM "{self.table_name}"'
        cursor.execute(get_all_query)

        records = cursor.fetchall()
        records = self.create_record_object(records, many=True)

        return jsonify({"message": "records found", "results": records}), 200

    def get_record_by_id(self, record_id):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400
        get_by_id_query = f"""SELECT {",".join(self.return_fields)} FROM "{self.table_name}"
        WHERE {self.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({"message": "record not found"}), 404

        return jsonify({"message": "record found", "results": self.create_record_object(record)}), 200

    def update_record(self, record_id):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400
        post_data = request.json
        update_fields = self.post_data_fields.copy()

        if "updated_at" in self.return_fields:
            update_fields.append("updated_at")
            post_data["updated_at"] = datetime_now()

        get_by_id_query = f"""SELECT {",".join(update_fields)} FROM "{self.table_name}"
        WHERE {self.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({"message": "record not found"}), 404

        update_query_fields = ",".join(f"{field} = %s" for field in update_fields)

        update_query = f"""UPDATE "{self.table_name}"
        SET {update_query_fields}
        WHERE {self.primary_key} = %s RETURNING {",".join(self.return_fields)}"""

        try:
            cursor.execute(update_query, (*[post_data.get(field, value) for (field, value) in zip(update_fields, record)], record_id))
            record = cursor.fetchone()
            connection.commit()
        except:
            connection.rollback()
            return jsonify({"message": "unable to update record"}), 400
        return jsonify({"message": "record updated", "results": self.create_record_object(record)}), 200

    def record_activity(self, record_id, active_field="active"):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400
        get_by_id_query = f"""SELECT {active_field} FROM "{self.table_name}"
        WHERE {self.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({"message": "record not found"}), 404

        [active] = record

        activity_query = f"""UPDATE "{self.table_name}"
        SET {active_field} = %s
        WHERE {self.primary_key} = %s RETURNING {",".join(self.return_fields)}"""
        active = not active
        cursor.execute(activity_query, (active, record_id))
        record = cursor.fetchone()
        connection.commit()

        return jsonify({"message": f"record {'activated' if active else 'deactivated'}", "results": self.create_record_object(record)}), 200

    def delete_record(self, record_id):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400
        get_by_id_query = f"""SELECT {self.primary_key} FROM "{self.table_name}"
        WHERE {self.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({"message": "record not found"}), 404

        [record_id] = record

        delete_query = f"""DELETE FROM "{self.table_name}"
        WHERE {self.primary_key} = %s"""
        try:
            cursor.execute(delete_query, (record_id,))
            connection.commit()
        except:
            connection.rollback()
            return jsonify({"message": "unable to delete record"}), 400

        return jsonify({"message": "record deleted"}), 200
