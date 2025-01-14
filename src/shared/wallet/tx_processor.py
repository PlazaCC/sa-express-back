from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.enums.user_status_enum import USER_STATUS

from src.shared.wallet.vault_processor import VaultProcessor
from src.shared.wallet.instructions.transfer import TXTransferInstruction

class TXProcessor:
    MAX_INSTRUCTIONS=1

    def __init__(self, cache, repository, pay_gate):
        self.cache = cache
        self.repository = repository

        self.pay_gate = pay_gate
        self.vault_proc = VaultProcessor(cache, repository)

    async def sign(self, signer: User, tx: TX) -> str | None:
        # validate tx fields and instructions fields
        
        # validate signer access
        signer_access_error = self.validate_signer_access(signer, tx)

        if signer_access_error is not None:
            return signer_access_error

        # vault_proc -> lock all

        # validate instructions execution

        # commit ready ?

        # call paygate and wait webhook
        # commit tx

        # vault_proc -> unlock all
        return None
    
    def validate_signer_access(self, signer: User, tx: TX) -> str | None:
        for instruction in tx.instructions:
            signer_access_error = instruction.validate_signer_access(signer)

            if signer_access_error is not None:
                return signer_access_error

        return None

    async def commit(self, tx: TX):
        pass
