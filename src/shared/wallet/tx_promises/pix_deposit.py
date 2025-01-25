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

        api_res = await tx_proc.paygate.post_pix_deposit(paygate_ref, self.amount)

        if 'error' in api_res:
            return TXLogs.failed(api_res['error']['message'])

        api_data = api_res['data']

        data = {
            'paygate_tx_id': api_data['transaction']['id'],
            'pix_qrcode': api_data['payment']['qrCode']
        }
        
        log = TXLogs.successful(data)

        log.populate_sign_data = lambda: ([
            ('paygate_ref', paygate_ref),
            ('paygate_tx_id', data['paygate_tx_id']),
            ('pix_qrcode', data['pix_qrcode']),
        ])

        return log