from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Shippings" (
    shipping_id UUID NOT NULL,
    order_id UUID NOT NULL,
    shipping_address VARCHAR NOT NULL,
    shipping_label VARCHAR NOT NULL,
    shipping_cost NUMERIC NOT NULL,
    tracking_number VARCHAR NOT NULL,
    shipping_status VARCHAR NOT NULL,
    shipped_date TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (shipping_id),
    FOREIGN KEY (order_id) REFERENCES "Orders" (order_id)
)""")

connection.commit()

def base_shipping_object(shipping):
    [shipping_id, order_id, shipping_address, shipping_label, shipping_cost, tracking_number, shipping_status, shipped_date] = shipping

    print(type(shipped_date))

    return {
        "shipping_id": shipping_id,
        "order_id": order_id,
        "shipping_address": shipping_address,
        "shipping_label": shipping_label,
        "shipping_cost": shipping_cost,
        "tracking_number": tracking_number,
        "shipping_status": shipping_status,
        "shipped_date": shipped_date and shipped_date.isoformat()
    }
