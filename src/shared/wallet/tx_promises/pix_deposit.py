from decimal import Decimal

from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXPIXDepositPromise(TXBasePromise):
    tx_id: str
    instruction_id: int
    pix_key: PIXKey
    amount: Decimal
    paygate_response: dict | None
    
    def __init__(self, tx_id: str, instruction_id: int, pix_key: PIXKey, \
        amount: Decimal, paygate_response: dict | None = None):
        self.tx_id = tx_id
        self.instruction_id = instruction_id
        self.pix_key = pix_key
        self.amount = amount
        self.paygate_response = paygate_response

    def to_dict(self) -> dict:
        return {
            'tx_id': self.tx_id,
            'instruction_id': self.instruction_id,
            'pix_key': self.pix_key.to_dict(),
            'amount': str(self.amount),
            'paygate_response': self.paygate_response
        }
    
    def to_paygate_ref(self) -> str:
        return f'{self.tx_id}-INSTR-{self.instruction_id}'
    
    def is_resolved(self):
        return self.paygate_response is not None
    
    async def call(self, tx_proc):
        # paygate = tx_proc.paygate
        # api_res = await paygate.create_pix_url()
        pass
    
    async def resolve(self):
        pass