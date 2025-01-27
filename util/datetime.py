from datetime import datetime, timezone

def datetime_now():
    return datetime.now(timezone.utc).replace(microsecond=0)
