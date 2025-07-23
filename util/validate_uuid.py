from uuid import UUID

def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
        return True
    except Exception:
        return False
