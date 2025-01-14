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
        fields_error = self.validate_tx_fields_before_sign(tx)
        
        if fields_error is not None:
            return fields_error
        
        tx.user_id = signer.user_id
        tx.logs = []

        signer_access_error = self.validate_signer_access(signer, tx)

        if signer_access_error is not None:
            return signer_access_error

        # vault_proc -> lock all

        # validate instructions amounts & vault balances

        # commit ready ?

        # call paygate and wait webhook
        # commit tx

        # vault_proc -> unlock all
        return None
    
    def validate_tx_fields_before_sign(self, tx: TX) -> str | None:
        if tx.status != TX_STATUS.NEW:
            return 'Unsignable transaction status'

        if tx.sign_timestamp is not None:
            return 'Transaction already signed'
        
        if tx.commit_timestamp is not None:
            return 'Transaction already commited'

        num_instructions = len(tx.instructions)

        if num_instructions == 0:
            return 'Transaction without instructions'

        if num_instructions > TXProcessor.MAX_INSTRUCTIONS:
            return f'Transaction with too many instructions (MAX {TXProcessor.MAX_INSTRUCTIONS})'
        
        defined_vaults = {}

        for vault in tx.vaults:
            vault_key = vault.to_identity_key()

            if vault_key not in defined_vaults:
                defined_vaults[vault_key] = True

        for instruction in tx.instructions:
            for vault in instruction.get_vaults():
                vault_key = vault.to_identity_key()

                if vault_key in defined_vaults:
                    del defined_vaults[vault_key]

        if len(defined_vaults) != 0:
            return 'Transaction vault matching failed'
        
        return None
    
    def validate_signer_access(self, signer: User, tx: TX) -> str | None:
        for instruction in tx.instructions:
            signer_access_error = instruction.validate_signer_access(signer)

            if signer_access_error is not None:
                return signer_access_error

        return None

    async def commit(self, tx: TX):
        pass
