from src.shared.wallet.models.pix import PIXKey

class PayGateWrapper:
    def __init__(self):
        pass

    async def create_pix_url(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        pass

    async def pix_withdraw(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        pass