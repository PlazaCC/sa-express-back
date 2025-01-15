from typing import Any
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXBaseInstructionResult:
    @staticmethod
    def successful(promise: TXBasePromise | None = None) -> 'TXBaseInstructionResult':
        pass
    
    @staticmethod
    def failed(error: str) -> 'TXBaseInstructionResult':
        pass
    
    def __init__(self):
        pass

    def to_dict(self) -> dict:
        pass

    def with_error(self) -> bool:
        pass

    async def call_promise(self, tx_proc: Any) -> TXLogs | None:
        pass