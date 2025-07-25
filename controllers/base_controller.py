from flask import request, jsonify

from db import connection, cursor
from util.validate_uuid import validate_uuid4
from util.datetime import datetime_now

class BaseController:
    create_record_object = None
    model = None

    def add_record(self):
        post_data = request.json
        current_datetime = datetime_now()

        post_data["created_at"] = current_datetime
        post_data["updated_at"] = current_datetime

        new_record = self.model().load(post_data)
        new_record.generate_key()

        [fields, values] = zip(*new_record.dump_update().items())
        insert_query = f"""INSERT INTO "{new_record.tablename}" VALUES ({",".join(["%s" for _ in fields])}) RETURNING *"""
        try:
            cursor.execute(insert_query, (*values,))
            new_record.load(cursor.fetchone())
            connection.commit()
        except:
            connection.rollback()
            return jsonify({"message": "unable to add record"}), 400

        return jsonify({"message": "added record", "results": self.create_record_object(new_record)}), 201

    def get_all_records(self):
        get_all_query = f'SELECT * FROM "{self.model.tablename}"'
        cursor.execute(get_all_query)

        records = [self.model().load(record) for record in cursor.fetchall()]
        records = self.create_record_object(records, many=True)

        return jsonify({"message": "records found", "results": records}), 200

    def get_record_by_id(self, record_id):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400
        get_by_id_query = f"""SELECT * FROM "{self.model.tablename}"
        WHERE {self.model.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({"message": "record not found"}), 404
        
        record = self.model().load(record)

        return jsonify({"message": "record found", "results": self.create_record_object(record)}), 200

    def update_record(self, record_id):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400
        post_data = request.json

        post_data["updated_at"] = datetime_now()

        get_by_id_query = f"""SELECT * FROM "{self.model.tablename}"
        WHERE {self.model.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({"message": "record not found"}), 404

        update_record = self.model().load(record)
        key = getattr(update_record, update_record.primary_key)
        update_record.load(post_data)
        setattr(update_record, update_record.primary_key, key)

        [fields, values] = zip(*update_record.dump_update().items())
        update_query_fields = ",".join(f"{field} = %s" for field in fields)
        update_query = f"""UPDATE "{self.model.tablename}" SET {update_query_fields} WHERE {update_record.primary_key} = %s RETURNING *"""

        try:
            cursor.execute(update_query, (*values, getattr(update_record, update_record.primary_key)))
            update_record.load(cursor.fetchone())
            connection.commit()
        except:
            connection.rollback()
            return jsonify({"message": "unable to update record"}), 400
        return jsonify({"message": "record updated", "results": self.create_record_object(update_record)}), 200

    def record_activity(self, record_id, active_field="active"):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400
        get_by_id_query = f"""SELECT {active_field} FROM "{self.model.tablename}"
        WHERE {self.model.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({"message": "record not found"}), 404

        [active] = record

        activity_query = f"""UPDATE "{self.model.tablename}"
        SET {active_field} = %s
        WHERE {self.model.primary_key} = %s RETURNING * """
        active = not active
        cursor.execute(activity_query, (active, record_id))
        record = cursor.fetchone()
        record = self.model().load(record)
        connection.commit()

        return jsonify({"message": f"record {'activated' if active else 'deactivated'}", "results": self.create_record_object(record)}), 200

    def delete_record(self, record_id):
        if not validate_uuid4(record_id):
            return jsonify({"message": "invalid record id"}), 400
        get_by_id_query = f"""SELECT {self.model.primary_key} FROM "{self.model.tablename}"
        WHERE {self.model.primary_key} = %s"""
        cursor.execute(get_by_id_query, (record_id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({"message": "record not found"}), 404

        [record_id] = record

        delete_query = f"""DELETE FROM "{self.model.tablename}"
        WHERE {self.model.primary_key} = %s"""
        try:
            cursor.execute(delete_query, (record_id,))
            connection.commit()
        except:
            connection.rollback()
            return jsonify({"message": "unable to delete record"}), 400

        return jsonify({"message": "record deleted"}), 200

    def update_many_records(self):
        post_data = request.json
        update_data = post_data.get("update")

        record_ids = set()
        update_data_map = {}
        for record in update_data:
            record_id = record.get(self.model.primary_key)
            if validate_uuid4(record_id):
                record_ids.add(record_id)
                update_data_map[record_id] = record

        update_records = []
        if len(record_ids) > 0:
            select_query = f"""SELECT * from "{self.model.tablename}"
            WHERE {self.model.primary_key} IN %s"""
            cursor.execute(select_query, (tuple(record_ids),))

            records = cursor.fetchall()
            fields = self.model().dump_update().keys()
            values = f'({",".join("%s" for _ in fields)})'
            query_fields = ",".join(f'{field} = "t2".{field}' + ("::uuid" if "_id" in field else "::timestamp" if "_date" in field else "") for field in fields if field != self.model.primary_key)

            new_update_data = []
            for record in records:
                record = self.model().load(record)
                record_data = update_data_map[getattr(record, record.primary_key)]
                record_data["updated_at"] = datetime_now()
                record.load(record_data)
                update_records.append(record)
                new_update_data += record.dump_update().values()

            values = ",".join(values for _ in records)
            update_query = f"""UPDATE "{self.model.tablename}" SET
            {query_fields}
            FROM (VALUES
            {values}
            ) AS t2({",".join(fields)})
            WHERE "{self.model.tablename}".{self.model.primary_key} = "t2".{self.model.primary_key}::uuid"""

            cursor.execute(update_query, new_update_data)
            connection.commit()

        update_records = self.create_record_object(update_records, many=True)
        return jsonify({"message": "records updated", "results": update_records}), 200
