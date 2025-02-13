import time

def now_timestamp() -> int:
    return int(round(time.time() * 1000))