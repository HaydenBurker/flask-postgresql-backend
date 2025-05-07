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

class Total:
    users = 5
    orders = 10
    products = 10
    order_items = 20
    categories = 10
    products_categories = 20
    discounts = 10
    orders_discounts = 20
    shippings = 5
    payments = 10
    reviews = 20
    suppliers = 10
    product_suppliers = 20

def random_letters():
    random_length = random.randint(8, 15)
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
    current_date = datetime_now()

    records = []
    user_ids = []
    for _ in range(Total.users):
        id = str(uuid.uuid4())
        user_ids.append(id)
        records += [id, random_letters(), random_letters(), random_letters() + "@" + random_letters() + "." + random_letters(), random_letters(), True, current_date, current_date]
    create_records(records, "Users")

    records = []
    order_ids = []
    for _ in range(Total.orders):
        id = str(uuid.uuid4())
        user_id = random.choice(user_ids)
        order_ids.append(id)
        records += [id, user_id, current_date, current_date, random_letters(), random.randint(1, 10), True, current_date, current_date]
    create_records(records, "Orders")

    records = []
    product_ids = []
    for _ in range(Total.products):
        id = str(uuid.uuid4())
        user_id = random.choice(user_ids)
        product_ids.append(id)
        records += [id, random_letters(), random_letters(), random.randint(1, 10), random.randint(0, 10), user_id, current_date, current_date]
    create_records(records, "Products")

    records = []
    for _ in range(Total.order_items):
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        order_item_id = str(uuid.uuid4())
        records += [order_item_id, order_id, product_id, random.randint(1, 10), random.randint(1, 10)]
    create_records(records, "OrderItems")

    records = []
    category_ids = []
    for _ in range(10):
        category_id = str(uuid.uuid4())
        category_ids.append(category_id)
        records += [category_id, random_letters(), random_letters()]
    create_records(records, "Categories")

    records = []
    product_category_ids = set()
    for _ in range(Total.products_categories):
        product_id = random.choice(product_ids)
        category_id = random.choice(category_ids)

        id = (product_id, category_id)
        if id in product_category_ids:
            continue

        product_category_ids.add(id)
        records += [*id]
    create_records(records, "ProductsCategoriesXref")

    records = []
    discount_ids = []
    for _ in range(Total.discounts):
        discount_id = str(uuid.uuid4())
        discount_ids.append(discount_id)
        records += [discount_id, random_letters(), random_letters(), random.randint(1, 10), current_date, current_date, random.randint(1, 10)]
    create_records(records, "Discounts")

    records = []
    order_disount_ids = set()
    for _ in range(Total.order_items):
        order_id = random.choice(order_ids)
        discount_id = random.choice(discount_ids)

        id = (order_id, discount_id)
        if id in order_disount_ids:
            continue

        order_disount_ids.add(id)
        records += [*id]
    create_records(records, "OrdersDiscountsXref")

    records = []
    for order_id in random.sample(order_ids, Total.shippings):
        shipping_id = str(uuid.uuid4())
        records += [shipping_id, order_id, random_letters(), random_letters(), random.randint(1, 10), random_letters(), random_letters(), current_date]
    create_records(records, "Shippings")

    records = []
    for _ in range(Total.payments):
        payment_id = str(uuid.uuid4())
        order_id = random.choice(order_ids)
        records += [payment_id, order_id, random_letters(), current_date, random_letters(), random.randint(1, 10)]
    create_records(records, "Payments")

    records = []
    for _ in range(Total.reviews):
        review_id = str(uuid.uuid4())
        customer_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        records += [review_id, customer_id, product_id, random.randint(1, 5), random_letters(), current_date]
    create_records(records, "Reviews")

    records = []
    supplier_ids = []
    for _ in range(Total.suppliers):
        supplier_id = str(uuid.uuid4())
        supplier_ids.append(supplier_id)
        records += [supplier_id, random_letters(), random_letters(), random_letters(), random_letters(), random_letters(), True]
    create_records(records, "Suppliers")

    records = []
    product_supplier_ids = set()
    for _ in range(Total.product_suppliers):
        product_id = random.choice(product_ids)
        supplier_id = random.choice(supplier_ids)

        id = (product_id, supplier_id)
        if id in product_supplier_ids:
            continue

        product_supplier_ids.add(id)
        records += [*id, random.randint(1, 10), current_date]
    create_records(records, "ProductSuppliers")
    connection.commit()

if __name__ == "__main__":
    populate_database()
