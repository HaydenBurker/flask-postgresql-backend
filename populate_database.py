import string
import random
import uuid

from db import connection, cursor
from models.users import User
from models.orders import Order
from models.products import Product
from models.order_items import OrderItem
from models.categories import Category
from models.products_categories_xref import ProductCategory
from models.discounts import Discount
from models.orders_discounts_xref import OrderDiscount
from models.shippings import Shipping
from models.payments import Payment
from models.reviews import Review
from models.suppliers import Supplier
from models.product_suppliers import ProductSupplier
from util.datetime import datetime_now

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

def create_records(records, model):
    fields = model().dump_update().keys()
    record_field_count = len(fields)
    user_count = len(records) // record_field_count
    query = f"""INSERT INTO "{model.tablename}" ({",".join(fields)}) VALUES """
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
    create_records(records, User)

    records = []
    order_ids = []
    for _ in range(Total.orders):
        id = str(uuid.uuid4())
        user_id = random.choice(user_ids)
        order_ids.append(id)
        records += [id, user_id, current_date, current_date, random_letters(), random.randint(1, 10), True, current_date, current_date]
    create_records(records, Order)

    records = []
    product_ids = []
    for _ in range(Total.products):
        id = str(uuid.uuid4())
        user_id = random.choice(user_ids)
        product_ids.append(id)
        records += [id, random_letters(), random_letters(), random.randint(1, 10), random.randint(0, 10), user_id, current_date, current_date]
    create_records(records, Product)

    records = []
    for _ in range(Total.order_items):
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        order_item_id = str(uuid.uuid4())
        records += [order_item_id, order_id, product_id, random.randint(1, 10), random.randint(1, 10)]
    create_records(records, OrderItem)

    records = []
    category_ids = []
    for _ in range(10):
        category_id = str(uuid.uuid4())
        category_ids.append(category_id)
        records += [category_id, random_letters(), random_letters()]
    create_records(records, Category)

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
    create_records(records, ProductCategory)

    records = []
    discount_ids = []
    for _ in range(Total.discounts):
        discount_id = str(uuid.uuid4())
        discount_ids.append(discount_id)
        records += [discount_id, random_letters(), random_letters(), random.randint(1, 10), current_date, current_date, random.randint(1, 10)]
    create_records(records, Discount)

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
    create_records(records, OrderDiscount)

    records = []
    for order_id in random.sample(order_ids, Total.shippings):
        shipping_id = str(uuid.uuid4())
        records += [shipping_id, order_id, random_letters(), random_letters(), random.randint(1, 10), random_letters(), random_letters(), current_date]
    create_records(records, Shipping)

    records = []
    for _ in range(Total.payments):
        payment_id = str(uuid.uuid4())
        order_id = random.choice(order_ids)
        records += [payment_id, order_id, random_letters(), current_date, random_letters(), random.randint(1, 10)]
    create_records(records, Payment)

    records = []
    for _ in range(Total.reviews):
        review_id = str(uuid.uuid4())
        customer_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        records += [review_id, customer_id, product_id, random.randint(1, 5), random_letters(), current_date]
    create_records(records, Review)

    records = []
    supplier_ids = []
    for _ in range(Total.suppliers):
        supplier_id = str(uuid.uuid4())
        supplier_ids.append(supplier_id)
        records += [supplier_id, random_letters(), random_letters(), random_letters(), random_letters(), random_letters(), True]
    create_records(records, Supplier)

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
    create_records(records, ProductSupplier)
    connection.commit()

if __name__ == "__main__":
    populate_database()
