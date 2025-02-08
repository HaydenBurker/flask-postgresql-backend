from datetime import datetime

def serialize(obj):
    if type(obj) == datetime:
        return obj and obj.isoformat()
    return obj

def base_record_object(record, fields):
    return {k: serialize(v) for (k, v) in zip(fields, record)}
