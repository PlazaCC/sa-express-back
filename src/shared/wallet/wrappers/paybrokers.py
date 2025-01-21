from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.wrappers.paybrokers import IWalletPayGate

class Paybrokers(IWalletPayGate):
    def __init__(self):
        pass
    
    ### PIX ###
    async def create_pix_url(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        pass
    
    async def pix_withdraw(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        pass