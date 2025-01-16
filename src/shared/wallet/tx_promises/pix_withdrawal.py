from typing import Any
from decimal import Decimal

from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXPIXWithdrawalPromise(TXBasePromise):
    tx_id: str
    instruction_id: int
    pix_key: PIXKey
    amount: Decimal
    resolved: bool
    
    def __init__(self, tx_id: str, instruction_id: int, pix_key: PIXKey, \
        amount: Decimal, resolved: bool):
        self.tx_id = tx_id
        self.instruction_id = instruction_id
        self.pix_key = pix_key
        self.amount = amount
        self.resolved = resolved

    def to_dict(self) -> dict:
        return {
            'tx_id': self.tx_id,
            'instruction_id': self.instruction_id,
            'pix_key': self.pix_key.to_dict(),
            'amount': str(self.amount),
            'resolved': self.resolved
        }
    
    def to_paygate_ref(self) -> str:
        return f'TX={self.tx_id}&INSTR={self.instruction_id}'
    
    def to_log_key(self) -> str:
        return f'INSTR={self.instruction_id}'
    
    async def call(self, tx_proc: Any) -> TXLogs:
        pass