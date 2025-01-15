from typing import Any
from decimal import Decimal

from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXPIXDepositPromise(TXBasePromise):
    tx_id: str
    instruction_id: int
    pix_key: PIXKey
    amount: Decimal
    
    def __init__(self, tx_id: str, instruction_id: int, pix_key: PIXKey, \
        amount: Decimal):
        self.tx_id = tx_id
        self.instruction_id = instruction_id
        self.pix_key = pix_key
        self.amount = amount

    def to_dict(self) -> dict:
        return {
            'tx_id': self.tx_id,
            'instruction_id': self.instruction_id,
            'pix_key': self.pix_key.to_dict(),
            'amount': str(self.amount)
        }
    
    def to_paygate_ref(self) -> str:
        return f'{self.tx_id}-INSTR-{self.instruction_id}'
    
    async def call(self, tx_proc: Any) -> TXLogs:
        paygate_ref = self.to_paygate_ref()

        api_res = await tx_proc.paygate.create_pix_url(paygate_ref)
        
        # if not api_res['success']:
        #     return api_res['error'], None
        
        # return None, api_res['data']

        if api_res['error']:
            return 

        return TXLogs.successful(data: dict | None = None)