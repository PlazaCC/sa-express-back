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

    async def sign(self, signer: User, tx: TX):
        have_access = self.verify_signer_vault_access(signer, tx)

        # stage tx

        # commit ready ?

        # call paygate and wait webhook
        # execute instructions and update vaults

        # vault_rpoc -> unlock all
        pass

    def verify_signer_vault_access(self, signer: User, tx: TX):
        for instruction in tx.instructions:
            instruction.validate_signer_access(signer)

        quit()
        pass

    async def stage(self, signer: User, tx: TX):
        # validate signer access on vaults


        # vault_proc -> lock all

        # validate if possible to execute instructions
        # stage instructions

        # return if pending commit
        pass

    async def commit(self, tx: TX):
        pass
