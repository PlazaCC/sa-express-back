from decimal import Decimal

from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXPIXDepositPromise(TXBasePromise):
    pix_key: PIXKey
    amount: Decimal
    paygate_response: dict | None
    
    def __init__(self, pix_key: PIXKey, amount: Decimal, paygate_response: dict | None = None):
        self.pix_key = pix_key
        self.amount = amount
        self.paygate_response = paygate_response

    def to_dict(self):
        return {
            'pix_key': self.pix_key.to_dict(),
            'amount': str(self.amount),
            'paygate_response': self.paygate_response
        }
    
    def is_resolved(self):
        return self.paygate_response is not None
    
    async def call(self, tx_proc):
        # pay_gate = tx_proc.pay_gate
        # api_res = await pay_gate.create_pix_url()
        pass
    
    async def resolve(self):
        pass