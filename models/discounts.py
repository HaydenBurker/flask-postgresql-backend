from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Discounts" (
    discount_id UUID NOT NULL,
    discount_code VARCHAR NOT NULL,
    discount_type VARCHAR,
    discount_value NUMERIC NOT NULL,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    min_order_amount INTEGER,
    PRIMARY KEY (discount_id)
)""")

connection.commit()

def base_discount_object(discount):
    [discount_id, discount_code, discount_type, discount_value, start_date, end_date, min_order_amount] = discount

    return {
        "discount_id": discount_id,
        "discount_code": discount_code,
        "discount_type": discount_type,
        "discount_value": discount_value,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "min_order_amount": min_order_amount,
    }
