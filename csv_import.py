import sys
import csv
import uuid
from types import FunctionType
from db import connection, cursor
from util.datetime import datetime_now

table_fields = {
    "Users": {
        "fields": ["user_id", "first_name", "last_name", "email", "password", "active", "created_at", "updated_at"],
        "default_values": [None, "", "", "", "", True, None, None]
    },
    "Orders": {
        "fields": ["order_id", "customer_id", "order_date", "shipping_date", "status", "total_amount", "active", "created_at", "updated_at"],
        "default_values": [None, None, None, None, "", 0, True, None, None]
    },
    "Shippings": {
        "fields": ["shipping_id", "order_id", "shipping_address", "shipping_label", "shipping_cost", "tracking_number", "shipping_status", "shipped_date"],
        "default_values": [None, None, "", "", "", "", ""]
    },
    "Payments": {
        "fields": ["payment_id", "order_id", "payment_method", "payment_date", "payment_status", "payment_amount"],
        "default_values": [None, None, "", None, "", 0]
    },
    "OrdersDiscountsXref": {
        "fields": ["order_id", "discount_id"],
        "default_values": [None, None]
    },
    "Discounts": {
        "fields": ["discount_id", "discount_code", "discount_type", "discount_value", "start_date", "end_date", "min_order_amount"],
        "default_values": [None, "", "", 0, None, None, 0]
    },
    "OrderItems": {
        "fields": ["order_item_id", "order_id", "product_id", "quantity", "unit_price"],
        "default_values": [None, None, None, 0, 0]
    },
    "Products": {
        "fields": ["product_id", "name", "price", "stock_quantity", "created_by_id", "created_at", "updated_at"],
        "default_values": [None, "", 0, 0, None, None, None]
    },
    "ProductsCategoriesXref": {
        "fields": ["product_id", "category_id"],
        "default_values": [None, None]
    },
    "Categories": {
        "fields": ["category_id", "name", "description"],
        "default_values": [None, "", ""]
    },
    "Reviews": {
        "fields": ["review_id", "customer_id", "product_id", "rating", "comment", "created_at"],
        "default_values": [None, None, None, 0, "", None]
    },
    "ProductSuppliers": {
        "fields": ["product_id", "supplier_id", "supply_price", "supply_date"],
        "default_values": [None, None, 0, None]
    },
    "Suppliers": {
        "fields": ["supplier_id", "company_name", "contact_name", "email", "phone_number", "address", "active"],
        "default_values": [None, "", "", "", "", "", True]
    }
}

def import_table(table_name, fields, default_values, file_name):
    with open(f"csv/import/{file_name}", "r") as import_file:
        query = f'INSERT INTO "{table_name}" ({",".join(fields)}) VALUES '
        values = f'({",".join("%s" for _ in fields)})'
        csv_reader = csv.DictReader(import_file)

        records = []
        for row in csv_reader:
            record_row = [row[field] for field in fields]
            record_row = [default_values[i] if value == "" else value for i, value in enumerate(record_row)]
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

        if table_name in table_fields:
            fields = table_fields[table_name]["fields"]
            default_values = table_fields[table_name]["default_values"]
            import_table(table_name, fields, default_values, file_name)

    elif len(sys.argv) > 1:
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
