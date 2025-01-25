from datetime import datetime

def now_timestamp() -> str:
    return str(int(datetime.now().timestamp() * 1000))