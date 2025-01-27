from abc import ABC, abstractmethod

from src.shared.wallet.decimal import Decimal
from src.shared.wallet.models.pix import PIXKey

class IWalletPayGate(ABC):
    ### OVERRIDE METHODS ###

    ### PIX ###
    @abstractmethod
    async def post_pix_deposit(self, tx_id: str, nonce: str, amount: Decimal) -> dict:
        pass
    
    @abstractmethod
    async def post_pix_withdrawal(self, tx_id: str, nonce: str, amount: Decimal, pix_key: PIXKey) -> dict:
        pass