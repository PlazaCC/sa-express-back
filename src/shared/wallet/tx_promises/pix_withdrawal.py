from typing import Any

from src.shared.wallet.decimal import Decimal
from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXPIXWithdrawalPromise(TXBasePromise):
    tx_id: str
    instr_index: int
    pix_key: PIXKey
    amount: Decimal
    
    def __init__(self, tx_id: str, instr_index: int, pix_key: PIXKey, \
        amount: Decimal):
        self.tx_id = tx_id
        self.instr_index = instr_index
        self.pix_key = pix_key
        self.amount = amount

    def to_dict(self) -> dict:
        return {
            'tx_id': self.tx_id,
            'instr_index': self.instr_index,
            'pix_key': self.pix_key.to_dict(),
            'amount': str(self.amount)
        }
    
    def to_paygate_ref(self) -> str:
        return f'TX={self.tx_id}&INSTR={self.instr_index}'
    
    async def call(self, tx_proc: Any) -> TXLogs:
        paygate_ref = self.to_paygate_ref()

        api_res = await tx_proc.paygate.post_pix_withdrawal(self.pix_key, paygate_ref)

        log_key = TXLogs.get_instruction_log_key(self.instr_index)

        if 'error' in api_res:
            return TXLogs.failed(log_key, api_res['error'])
        
        log = TXLogs.successful(log_key)
        
        log.populate_sign_data = lambda: ([
            ('paygate_ref', paygate_ref),
            ('pix_key', self.pix_key.to_dict())
        ])
            
        return log