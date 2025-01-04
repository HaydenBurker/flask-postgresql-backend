import os
import psycopg2

connection = psycopg2.connect(
    database=os.getenv("DATABASE_NAME"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT")
)
cursor = connection.cursor()
