from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.enums.user_status_enum import USER_STATUS

from src.shared.wallet.vault_processor import VaultProcessor

class TXProcessor:
    MAX_INSTRUCTIONS=6

    def __init__(self, cache, repository, pay_gate):
        self.cache = cache
        self.repository = repository

        self.pay_gate = pay_gate
        self.vault_proc = VaultProcessor(cache, repository)

    def create_tx(self):
        pass

    async def validate_tx(self, tx):
        pass
    
    async def process(self):
        pass
