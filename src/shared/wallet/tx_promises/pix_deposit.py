from typing import Any

from src.shared.wallet.decimal import Decimal
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXPIXDepositPromise(TXBasePromise):
    tx_id: str
    nonce: str
    amount: Decimal
    ref_id: str

    def __init__(self, tx_id: str, nonce: str, amount: Decimal, ref_id: str):
        self.tx_id = tx_id
        self.nonce = nonce
        self.amount = amount
        self.ref_id = ref_id

    def to_dict(self) -> dict:
        return {
            'tx_id': self.tx_id,
            'nonce': self.nonce,
            'amount': str(self.amount),
            'ref_id': self.ref_id
        }
    
    async def call(self, tx_proc: Any) -> TXLogs:
        api_res = await tx_proc.paygate.post_pix_deposit(self.tx_id, self.nonce, self.amount, \
            self.ref_id)

        if 'error' in api_res:
            return TXLogs.failed(api_res['error']['message'])

        api_data = api_res['data']

        data = {
            'paygate_tx_id': api_data['transaction']['id'],
            'pix_qrcode': api_data['payment']['qrCode']
        }
        
        log = TXLogs.successful(data)

        log.populate_sign_data = lambda: ([
            ('paygate_tx_id', data['paygate_tx_id']),
            ('pix_qrcode', data['pix_qrcode']),
        ])

        return log