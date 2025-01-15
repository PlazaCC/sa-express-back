from src.shared.wallet.utils import now_timestamp
from src.shared.wallet.tx_instruction_results.base import TXBaseInstructionResult

class TXTransferInstructionResult(TXBaseInstructionResult):
    success: bool
    timestamp: str
    error: str

    @staticmethod
    def succesful():
        return TXTransferInstructionResult(success=True, timestamp=now_timestamp())
    
    @staticmethod
    def failed(error: str) -> 'TXTransferInstructionResult':
        return TXTransferInstructionResult(success=False, timestamp=now_timestamp(), error=error)

    def __init__(self, success: bool, timestamp: str, error: str = ''):
        self.success = success
        self.timestamp = timestamp
        self.error = error