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
    for _ in range(user_count):
        records += [str(uuid.uuid4()), random_letters(), random_letters(), random_letters(), random_letters(), True, current_date, current_date]

    cursor.execute(query, records)
    connection.commit()

if __name__ == "__main__":
    populate_database()
