from db import connection, cursor

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