from db import connection, cursor

from .base_model import Model

class Supplier(Model):
    primary_key = "supplier_id"
    tablename = "Suppliers"

    def __init__(self, supplier_id=None, company_name="", contact_name="", email="", phone_number="", address="", active=True):
        self.supplier_id = supplier_id
        self.company_name = company_name
        self.contact_name = contact_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.active = active
        self.set_fields()

cursor.execute("""CREATE TABLE IF NOT EXISTS "Suppliers" (
    supplier_id UUID NOT NULL,
    company_name VARCHAR NOT NULL,
    contact_name VARCHAR,
    email VARCHAR,
    phone_number VARCHAR,
    address VARCHAR,
    active BOOLEAN NOT NULL,
    PRIMARY KEY (supplier_id),
    UNIQUE (company_name)
)""")

connection.commit()
