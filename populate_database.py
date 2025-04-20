import string
import random
import uuid

from db import connection, cursor
from util.datetime import datetime_now

table_fields = {
    "Users": ["user_id", "first_name", "last_name", "email", "password", "active", "created_at", "updated_at"],
    "Orders": ["order_id", "customer_id", "order_date", "shipping_date", "status", "total_amount", "active", "created_at", "updated_at"],
    "Shippings": ["shipping_id", "order_id", "shipping_address", "shipping_label", "shipping_cost", "tracking_number", "shipping_status", "shipped_date"],
    "Payments": ["payment_id", "order_id", "payment_method", "payment_date", "payment_status", "payment_amount"],
    "OrdersDiscountsXref": ["order_id", "discount_id"],
    "Discounts": ["discount_id", "discount_code", "discount_type", "discount_value", "start_date", "end_date", "min_order_amount"],
    "OrderItems": ["order_item_id", "order_id", "product_id", "quantity", "unit_price"],
    "Products": ["product_id", "name", "description", "price", "stock_quantity", "created_by_id", "created_at", "updated_at"],
    "ProductsCategoriesXref": ["product_id", "category_id"],
    "Categories": ["category_id", "name", "description"],
    "Reviews": ["review_id", "customer_id", "product_id", "rating", "comment", "created_at"],
    "ProductSuppliers": ["product_id", "supplier_id", "supply_price", "supply_date"],
    "Suppliers": ["supplier_id", "company_name", "contact_name", "email", "phone_number", "address", "active"]
}

def random_letters():
    random_length = random.randint(3, 10)
    return "".join(random.choice((string.ascii_lowercase)) for _ in range(random_length))

def create_records(records, table_name):
    fields = table_fields[table_name]
    record_field_count = len(fields)
    user_count = len(records) // record_field_count
    query = f"""INSERT INTO "{table_name}" ({",".join(fields)}) VALUES """
    values = f"({','.join('%s' for _ in range(record_field_count))})"
    query += ",".join(values for _ in range(user_count))
    cursor.execute(query, records)

def populate_database():
    user_count = 5
    current_date = datetime_now()

    records = []
    user_ids = []
    for _ in range(user_count):
        id = str(uuid.uuid4())
        user_ids.append(id)
        records += [id, random_letters(), random_letters(), random_letters() + "@" + random_letters() + "." + random_letters(), random_letters(), True, current_date, current_date]
    create_records(records, "Users")

    records = []
    order_ids = []
    for user_id in user_ids:
        id = str(uuid.uuid4())
        order_ids.append(id)
        records += [id, user_id, current_date, current_date, random_letters(), random.randint(1, 10), True, current_date, current_date]
    create_records(records, "Orders")

    records = []
    product_ids = []
    for user_id in user_ids:
        id = str(uuid.uuid4())
        product_ids.append(id)
        records += [id, random_letters(), random_letters(), random.randint(1, 10), random.randint(0, 10), user_id, current_date, current_date]
    create_records(records, "Products")

    records = []
    for _ in range(20):
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        order_item_id = str(uuid.uuid4())
        records += [order_item_id, order_id, product_id, random.randint(1, 10), random.randint(1, 10)]
    create_records(records, "OrderItems")

    records = []
    for _ in range(10):
        category_id = str(uuid.uuid4())
        records += [category_id, random_letters(), random_letters()]
    create_records(records, "Categories")
    connection.commit()

if __name__ == "__main__":
    populate_database()
