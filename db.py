import os
import contextlib
import psycopg2

@contextlib.contextmanager
def get_connection():
    try:
        connection = psycopg2.connect(
            database=os.getenv("DATABASE_NAME"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT")
        )
        cursor = connection.cursor()
        yield connection, cursor
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
