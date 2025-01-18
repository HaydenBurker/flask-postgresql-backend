from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Categories" (
    category_id UUID NOT NULL,
    name VARCHAR NOT NULL UNIQUE,
    description VARCHAR,
    UNIQUE (name),
    PRIMARY KEY (category_id)
)""")

connection.commit()

def base_category_object(category):
    [category_id, name, description] = category
    return {
        "category_id": category_id,
        "name": name,
        "description": description
    }
