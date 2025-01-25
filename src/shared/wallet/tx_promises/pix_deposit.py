from typing import Any

from src.shared.wallet.decimal import Decimal
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXPIXDepositPromise(TXBasePromise):
    tx_id: str
    amount: Decimal
    
    def __init__(self, tx_id: str, amount: Decimal):
        self.tx_id = tx_id
        self.amount = amount

    def to_dict(self) -> dict:
        return {
            'tx_id': self.tx_id,
            'amount': str(self.amount)
        }
    
    def to_paygate_ref(self) -> str:
        return f'TX={self.tx_id}'
    
    async def call(self, tx_proc: Any) -> TXLogs:
        paygate_ref = self.to_paygate_ref()

        api_res = await tx_proc.paygate.post_pix_deposit(paygate_ref)

        if 'error' in api_res:
            return TXLogs.failed(api_res['error'])

        api_data = api_res['data']

        data = {
            'pix_url': api_data['pix_url'],
        }
        
        log = TXLogs.successful(data)

        log.populate_sign_data = lambda: ([
            ('paygate_ref', paygate_ref),
            ('pix_url', data['pix_url']),
        ])

        return log