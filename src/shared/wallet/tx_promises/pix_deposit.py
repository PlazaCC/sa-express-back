from typing import Any
from decimal import Decimal

from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXPIXDepositPromise(TXBasePromise):
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
        api_res = await tx_proc.paygate.create_pix_url(self.pix_key, self.to_paygate_ref())

        log_key = TXLogs.get_instruction_log_key(self.instr_index)

        if 'error' in api_res:
            return TXLogs.failed(log_key, api_res['error'])

        data = api_res['data']

        log = TXLogs.successful(log_key, data)

        log.populate_sign_data = lambda: [ ('pix_url', data['pix_url']) ]

        return log