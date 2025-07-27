import sys
import csv
import uuid

from db import connection, cursor

from models.users import User
from util.datetime import datetime_now
from util.models import table_name_to_model


def import_table(model, file_name):
    fields = model().dump_update().keys()

    with open(f"csv/import/{file_name}", "r") as import_file:
        query = f'INSERT INTO "{model.tablename}" ({",".join(fields)}) VALUES '
        values = f'({",".join("%s" for _ in fields)})'
        csv_reader = csv.DictReader(import_file)

        records = []
        for row in csv_reader:
            row = {k:v for k, v in row.items() if v != ""}
            record_row = tuple(model().load(row).dump_update().values())
            records += record_row

        record_count = csv_reader.line_num - 1

        query += ",".join(values for _ in range(record_count))
        try:
            cursor.execute(query, records)
            connection.commit()
        except:
            connection.rollback()
            print("failed to add records")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        table_name = sys.argv[1]
        file_name = sys.argv[2]

        model = table_name_to_model(table_name)
        if model:
            import_table(model, file_name)

    elif len(sys.argv) > 1:
        with open(f"csv/import/{sys.argv[1]}", "r") as import_file:
            csv_reader = csv.DictReader(import_file)
            fields = User().dump_update().keys()

            insert_query = f"""INSERT INTO "Users" ({",".join(fields)})
            VALUES """
            values = "(%s, %s, %s, %s, %s, %s, %s, %s)"

            records = []
            current_date = datetime_now()
            default_values = {field: value for field, value in zip(fields, [lambda: str(uuid.uuid4()), "", "", "", "", True, current_date, current_date])}

            for row in csv_reader:
                row = {k:v for k, v in row.items() if v != ""}
                row["user_id"] = row.get("user_id", str(uuid.uuid4()))
                row["created_at"] = row.get("created_at", current_date)
                row["updated_at"] = row.get("updated_at", current_date)
                record_row = tuple(User().load(row).dump_update().values())
                records += record_row

            record_count = csv_reader.line_num - 1

            if record_count:
                select_query = """SELECT user_id FROM "Users" WHERE email = %s"""
                cursor.execute(select_query, (records[3],))
                user = cursor.fetchone()

                if not user:
                    insert_query += ",".join(values for _ in range(csv_reader.line_num - 1))
                    cursor.execute(insert_query, records)
                    connection.commit()
