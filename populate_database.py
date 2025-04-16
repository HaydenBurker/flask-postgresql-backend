import string
import random
import uuid

from db import connection, cursor
from util.datetime import datetime_now


def random_letters():
    random_length = random.randint(3, 10)
    return "".join(random.choice((string.ascii_lowercase)) for _ in range(random_length))

def populate_database():
    user_count = 5
    query = """INSERT INTO "Users" (user_id, first_name, last_name, email, password, active, created_at, updated_at) VALUES """
    values = "(%s, %s, %s, %s, %s, %s, %s, %s)"
    query += ",".join(values for _ in range(user_count))
    current_date = datetime_now()

    records = []
    user_ids = []
    for _ in range(user_count):
        id = str(uuid.uuid4())
        user_ids.append(id)
        records += [id, random_letters(), random_letters(), random_letters() + "@" + random_letters() + "." + random_letters(), random_letters(), True, current_date, current_date]
    cursor.execute(query, records)

    query = """INSERT INTO "Orders" (order_id, customer_id, order_date, shipping_date, status, total_amount, active, created_at, updated_at) VALUES"""
    values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    query += ",".join(values for _ in range(user_count))

    records = []
    order_ids = []
    for user_id in user_ids:
        id = str(uuid.uuid4())
        order_ids.append(id)
        records += [id, user_id, current_date, current_date, random_letters(), random.randint(1, 10), True, current_date, current_date]

    cursor.execute(query, records)

    query = """INSERT INTO "Products" (product_id, name, description, price, stock_quantity, created_by_id, created_at, updated_at) VALUES"""
    values = "(%s, %s, %s, %s, %s, %s, %s, %s)"
    query += ",".join(values for _ in range(user_count))

    records = []
    product_ids = []
    for user_id in user_ids:
        id = str(uuid.uuid4())
        product_ids.append(id)
        records += [id, random_letters(), random_letters(), random.randint(1, 10), random.randint(0, 10), user_id, current_date, current_date]
    cursor.execute(query, records)
    connection.commit()

if __name__ == "__main__":
    populate_database()
