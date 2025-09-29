from db import connection, cursor

from .base_model import Model

class Category(Model):
    primary_key = "category_id"
    tablename = "Categories"

    def __init__(self, category_id=None, name="", description=""):
        self.category_id = category_id
        self.name = name
        self.description = description

    @classmethod
    def init_model(cls):
        super().init_model()

        cursor.execute("""CREATE TABLE IF NOT EXISTS "Categories" (
            category_id UUID NOT NULL,
            name VARCHAR NOT NULL UNIQUE,
            description VARCHAR,
            UNIQUE (name),
            PRIMARY KEY (category_id)
        )""")

        connection.commit()

Category.init_model()
