from db import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS "Users" (
        user_id UUID NOT NULL,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        email VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        ACTIVE BOOLEAN NOT NULL,
        UNIQUE (email),
        PRIMARY KEY (user_id)
);""")

connection.commit()
