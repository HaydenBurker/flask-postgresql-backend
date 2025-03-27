import sys
import csv

from db import cursor

table_fields = {
    "Users": ["user_id", "first_name", "last_name", "email", "password", "active", "created_at", "updated_at"],
    "Orders": ["order_id", "customer_id", "order_date", "shipping_date", "status", "total_amount", "active", "created_at", "updated_at"],
    "Payments": ["payment_id", "order_id", "payment_method", "payment_date", "payment_status", "payment_amount"]
}

def export_table(table_name, fields, file_name):
    with open(f"csv/export/{file_name}", "w") as export_file:
        query = f'SELECT {",".join(fields)} FROM "{table_name}"'
        cursor.execute(query)
        records = cursor.fetchall()

        csv_writer = csv.writer(export_file)
        csv_writer.writerow(fields)
        csv_writer.writerows(records)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        table_name = sys.argv[1]
        file_name = sys.argv[2]

        if table_name in table_fields:
            fields = table_fields[table_name]
            export_table(table_name, fields, file_name)
