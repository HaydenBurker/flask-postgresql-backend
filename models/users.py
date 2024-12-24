import psycopg2
from db import get_connection

# connection = psycopg2.connect(os.getenv("DATABASE_URI"))
connection = get_connection()
cursor = connection.cursor()

print(cursor.execute("""CREATE TABLE IF NOT EXISTS "Users" (
        user_id UUID NOT NULL,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        email VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        ACTIVE BOOLEAN NOT NULL,
        UNIQUE (email),
        PRIMARY KEY (user_id)
);"""))

connection.commit()
# cursor.execute("""CREATE TABLE "Users" (
#                 user_id UUID NOT NULL,
#                 PRIMARY KEY (user_id)
#                 );""")
