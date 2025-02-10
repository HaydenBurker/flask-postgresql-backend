from datetime import datetime

def serialize(obj):
    if type(obj) == datetime:
        return obj and obj.isoformat()
    return obj

def base_record_object(record, fields):
    return {k: serialize(v) for (k, v) in zip(fields, record)}

def create_record_mapping(records, base_record_object, key=None, many=False):
    record_mapping = {}

    for record in records:
        if not key:
            record_key = record[-1]

        record = base_record_object(record)

        if key:
            record_key = record[key]

        if many:
            if not record_mapping.get(record_key):
                record_mapping[record_key] = [record]
            else:
                record_mapping[record_key].append(record)
        else:
            record_mapping[record_key] = record

    return record_mapping
