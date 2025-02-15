import sys
import csv
import uuid
from types import FunctionType
from db import connection, cursor
from util.datetime import datetime_now

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(f"csv/import/{sys.argv[1]}", "r") as import_file:
            csv_reader = csv.DictReader(import_file)
            fields = ["user_id", "first_name", "last_name", "email", "password", "active", "created_at", "updated_at"]

            insert_query = f"""INSERT INTO "Users" ({",".join(fields)})
            VALUES """
            values = "(%s, %s, %s, %s, %s, %s, %s, %s)"

            records = []
            current_date = datetime_now()
            default_values = {field: value for field, value in zip(fields, [lambda: str(uuid.uuid4()), "", "", "", "", True, current_date, current_date])}

            for row in csv_reader:
                record_row = [row[field] if field in row else default_values[field] for field in fields]
                record_row = tuple([value() if type(value) == FunctionType else value for value in record_row])
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
