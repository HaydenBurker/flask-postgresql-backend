import os
import psycopg2

def get_connection():
    print(os.getenv("DATABASE_URI"))
    connection = psycopg2.connect(
        database=os.getenv("DATABASE_NAME"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT")
    )

    print(connection)

    return connection
