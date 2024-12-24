import os
import psycopg2

def get_connection():
    connection = psycopg2.connect(
        database=os.getenv("DATABASE_NAME"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT")
    )

    return connection
