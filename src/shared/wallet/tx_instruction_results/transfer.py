from typing import Any

from src.shared.wallet.utils import now_timestamp
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_instruction_results.base import TXBaseInstructionResult
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXTransferInstructionResult(TXBaseInstructionResult):
    error: str
    timestamp: str
    promise: TXBasePromise | None

    @staticmethod
    def successful(promise: TXBasePromise | None = None) -> 'TXTransferInstructionResult':
        return TXTransferInstructionResult(
            error='',
            timestamp=now_timestamp(),
            promise=promise
        )
    
    @staticmethod
    def failed(error: str) -> 'TXTransferInstructionResult':
        return TXTransferInstructionResult(timestamp=now_timestamp(), error=error)

    def __init__(self, error: str, timestamp: str, promise: TXBasePromise | None = None):
        self.error = error
        self.timestamp = timestamp
        self.promise = promise

    def to_dict(self) -> dict:
        result = {
            'error': self.error,
            'timestamp': self.timestamp,
        }

        if self.promise is not None:
            result['promise'] = self.promise.to_dict()

        return result

    def with_error(self) -> bool:
        return self.error != ''

    async def call_promise(self, tx_proc: Any) -> TXLogs | None:
        if self.promise is None:
            return None

        return await self.promise.call(tx_proc)
        