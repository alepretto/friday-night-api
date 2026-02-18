from datetime import datetime
from zoneinfo import ZoneInfo


def to_local(dt: datetime):
    dt_local = dt.astimezone(ZoneInfo("America/Araguaina"))
    return dt_local.isoformat()
