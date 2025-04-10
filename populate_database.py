import string
import random
import uuid

from db import connection, cursor
from util.datetime import datetime_now


def random_letters():
    random_length = random.randint(3, 10)
    return "".join(random.choice((string.ascii_lowercase)) for _ in range(random_length))

def populate_database():
    query = """INSERT INTO "Users" (user_id, first_name, last_name, email, password, active, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    current_date = datetime_now()
    cursor.execute(query, (str(uuid.uuid4()), random_letters(), random_letters(), random_letters(), random_letters(), True, current_date, current_date))
    connection.commit()

if __name__ == "__main__":
    populate_database()
