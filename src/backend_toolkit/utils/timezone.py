from datetime import datetime
from zoneinfo import ZoneInfo

# change this if you want to use another timezone
IRAN_TZ = ZoneInfo("Asia/Tehran")

def now_iran() -> datetime:
    return datetime.now(IRAN_TZ)

def now_iran_str() -> str:
    """Returns: YYYY-MM-DD HH:MM:SS"""
    return now_iran().strftime("%Y-%m-%d %H:%M:%S")
