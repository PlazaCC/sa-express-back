from enum import Enum

class TXBaseInstruction:
    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXBaseInstruction':
        pass

    def __init__(self):
        pass

    def to_tx_snapshot(self) -> dict:
        pass

class TX_INSTRUCTION_TYPE(Enum):
    TRANSFER = 'TRANSFER'