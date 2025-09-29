from db import connection, cursor

from .base_model import Model

class User(Model):
    primary_key = "user_id"
    tablename = "Users"

    def __init__(self, user_id=None, first_name="", last_name="", email="", password="", active=True, created_at=None, updated_at=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

    def dump(self):
        obj = super().dump()
        del obj['password']
        return obj

    @classmethod
    def init_model(cls):
        super().init_model()

        cursor.execute("""CREATE TABLE IF NOT EXISTS "Users" (
            user_id UUID NOT NULL,
            first_name VARCHAR NOT NULL,
            last_name VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            password VARCHAR NOT NULL,
            active BOOLEAN NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
            UNIQUE (email),
            PRIMARY KEY (user_id)
        )""")

        connection.commit()

User.init_model()
