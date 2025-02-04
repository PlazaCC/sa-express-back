from enum import Enum

class TX_STATUS(Enum):
    NEW = 'NEW'
    SIGNED = 'SIGNED'
    COMMITTED = 'COMMITTED'