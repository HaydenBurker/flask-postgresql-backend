from db import get_connection

with get_connection() as [connection, cursor]:
    cursor.execute("""CREATE TABLE IF NOT EXISTS "Categories" (
            category_id UUID NOT NULL,
            name VARCHAR NOT NULL UNIQUE,
            UNIQUE (name),
            PRIMARY KEY (category_id)
    )""")

    connection.commit()
