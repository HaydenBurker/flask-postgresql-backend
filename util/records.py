from datetime import datetime

def serialize(obj):
    if type(obj) == datetime:
        return obj and obj.isoformat()
    return obj

def create_record_mapping(records, key=None, many=False):
    record_mapping = {}

    for record in records:
        record_key = getattr(record, key or record.primary_key)

        if many:
            record_mapping.setdefault(record_key, []).append(record.dump())
        else:
            record_mapping[record_key] = record.dump()

    return record_mapping
