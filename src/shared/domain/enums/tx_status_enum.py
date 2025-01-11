from enum import Enum

class TX_STATUS(Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"