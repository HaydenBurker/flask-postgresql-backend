from datetime import datetime

def serialize(obj):
    if type(obj) == datetime:
        return obj and obj.isoformat()
    return obj

def base_record_object(record, fields):
    return {k: serialize(v) for (k, v) in zip(fields, record)}

def get_nested_records(cursor, many, foreign_keys, primary_table, primary_key_column, base_record_object, fields=["*"]):
    foreign_records = []

    if foreign_keys:
        products_query = f"""SELECT {",".join(field for field in fields)} FROM "{primary_table}"
        WHERE {primary_key_column} {"IN" if many else "="} %s"""
        cursor.execute(products_query, (foreign_keys,))
        primary_records = cursor.fetchall()
        primary_records = [base_record_object(product) for product in primary_records]
        foreign_records = {product.get(primary_key_column): [] for product in primary_records}
        for record in primary_records:
            foreign_records[record.get(primary_key_column)].append(record)

    return foreign_records
