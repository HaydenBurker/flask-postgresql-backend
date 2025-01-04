from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Users" (
    user_id UUID NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    active BOOLEAN NOT NULL,
    UNIQUE (email),
    PRIMARY KEY (user_id)
)""")

connection.commit()
