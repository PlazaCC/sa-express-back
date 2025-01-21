from abc import ABC, abstractmethod
from src.shared.wallet.models.pix import PIXKey

class IWalletPayGate(ABC):
    ### OVERRIDE METHODS ###
    
    ### PIX ###
    @abstractmethod
    async def create_pix_url(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        pass
    
    @abstractmethod
    async def pix_withdraw(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        pass