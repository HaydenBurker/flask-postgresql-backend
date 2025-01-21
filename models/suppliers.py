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

def base_supplier_object(supplier):
    [supplier_id, company_name, contact_name, email, phone_number, address, active] = supplier

    return {
        "supplier_id": supplier_id,
        "company_name": company_name,
        "contact_name": contact_name,
        "email": email,
        "phone_number": phone_number,
        "address": address,
        "active": active
    }
