from abc import ABC, abstractmethod
from src.shared.wallet.models.pix import PIXKey

class IWalletPayGate(ABC):
    ### OVERRIDE METHODS ###

    ### PIX ###
    @abstractmethod
    async def post_pix_deposit(self, paygate_ref: str) -> dict:
        pass
    
    @abstractmethod
    async def post_pix_withdrawal(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        pass