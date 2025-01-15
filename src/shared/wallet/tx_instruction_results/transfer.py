from src.shared.wallet.utils import now_timestamp
from src.shared.wallet.tx_instruction_results.base import TXBaseInstructionResult
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXTransferInstructionResult(TXBaseInstructionResult):
    success: bool
    timestamp: str
    error: str
    promises: list[TXBasePromise]

    @staticmethod
    def succesful(promises: list[TXBasePromise] = []):
        return TXTransferInstructionResult(
            success=True, 
            timestamp=now_timestamp(), 
            error='', 
            promises=promises
        )
    
    @staticmethod
    def failed(error: str) -> 'TXTransferInstructionResult':
        return TXTransferInstructionResult(success=False, timestamp=now_timestamp(), error=error)

    def __init__(self, success: bool, timestamp: str, error: str = '', \
        promises: list[TXBasePromise] = []):
        self.success = success
        self.timestamp = timestamp
        self.error = error
        self.promises = promises