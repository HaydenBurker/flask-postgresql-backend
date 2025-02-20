import sys
import csv

from db import cursor

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(f"csv/export/{sys.argv[1]}", "w") as export_file:
            user_fields = ["user_id","first_name","last_name","email","password","active","created_at","updated_at"]
            users_query = f'SELECT {",".join(user_fields)} FROM "Users"'
            cursor.execute(users_query)
            users = cursor.fetchall()

            csv_writer = csv.writer(export_file)
            csv_writer.writerow(user_fields)
            csv_writer.writerows(users)
