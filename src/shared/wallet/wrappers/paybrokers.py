from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.wrappers.paygate import IWalletPayGate

class Paybrokers(IWalletPayGate):
    def __init__(self):
        pass
    
    ### PIX ###
    async def post_pix_deposit(self, paygate_ref: str) -> dict:
        pass
    
    async def post_pix_withdrawal(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        pass