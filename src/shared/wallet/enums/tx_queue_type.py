from enum import Enum

class TX_QUEUE_TYPE(Enum):
    CLIENT = 'CLIENT'
    SERVER_SINGLE = 'SERVER_SINGLE'
    SERVER_MULTI = 'SERVER_MULTI'