from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.wrappers.paygate import IWalletPayGate

class WalletPayGateMock(IWalletPayGate):
    def __init__(self):
        self.pending_payments = []

    ### OVERRIDE METHODS ###
    
    ### PIX ###
    async def post_pix_deposit(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        self.pending_payments.append(paygate_ref)

        return {
            'data': {
                'pix_url': '00020126330014BR.GOV.BCB.PIX0111000000000005204000053039865406150.005802BR5904joao6009sao paulo621605121121212121216304E551'
            }
        }
    
    async def post_pix_withdrawal(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        self.pending_payments.append(paygate_ref)

        return {}