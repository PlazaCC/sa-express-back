from decimal import Decimal

from src.shared.domain.entities.vault import Vault

from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.tx_promises.base import TXBasePromise

class TXPIXWithdrawalPromise(TXBasePromise):
    pix_key: PIXKey
    amount: Decimal
    vault: Vault
    resolved: bool
    error: str
    data: dict
    
    def __init__(self):
        pass

    async def call(self):
        pass

    async def resolve(self):
        pass