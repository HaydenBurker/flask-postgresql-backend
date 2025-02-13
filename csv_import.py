import sys
import csv
import uuid
from db import connection, cursor
from util.datetime import datetime_now

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(f"csv/import/{sys.argv[1]}", "r") as import_file:
            csv_reader = csv.reader(import_file)
            header = next(csv_reader)

            insert_query = """INSERT INTO "Users" (user_id, first_name, last_name, email, password, active, created_at, updated_at)
            VALUES """
            values = "(%s, %s, %s, %s, %s, %s, %s, %s)"

            records = []
            for row in csv_reader:
                row = tuple([str(uuid.uuid4()), *row, datetime_now(), datetime_now()])
                records += row

            record_count = csv_reader.line_num - 1

            if record_count:
                select_query = """SELECT user_id FROM "Users" WHERE email = %s"""
                cursor.execute(select_query, (records[3],))
                user = cursor.fetchone()

                if not user:
                    insert_query += ",".join(values for _ in range(csv_reader.line_num - 1))
                    cursor.execute(insert_query, records)
                    connection.commit()
