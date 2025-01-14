from decimal import Decimal

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault

from src.shared.wallet.enums.tx_instruction_type import TX_INSTRUCTION_TYPE
from src.shared.wallet.instructions.base import TXBaseInstruction

class TXTransferInstruction(TXBaseInstruction):
    from_vault: Vault
    to_vault: Vault
    amount: Decimal

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXTransferInstruction':
        return TXTransferInstruction(
            from_vault=Vault.from_tx_instr_snapshot(data['from_vault']),
            to_vault=Vault.from_tx_instr_snapshot(data['to_vault']),
            amount=data['amount']
        )
    
    def __init__(self, from_vault: Vault, to_vault: Vault, amount: Decimal):
        self.from_vault = from_vault
        self.to_vault = to_vault
        self.amount = amount

    def to_tx_snapshot(self) -> dict:
        return {
            'type': TX_INSTRUCTION_TYPE.TRANSFER.value,
            'from_vault': self.from_vault.to_tx_instr_snapshot(),
            'to_vault': self.to_vault.to_tx_instr_snapshot(),
            'amount': str(self.amount)
        }
    
    def validate_signer_access(self, signer: User) -> str | None:
        from_vault = self.from_vault

        if from_vault.type == VAULT_TYPE.SERVER_UNLIMITED:
            return self.validate_signer_access_from_server_unlimited(signer)
        
        if from_vault.type == VAULT_TYPE.SERVER_LIMITED:
            return self.validate_signer_access_from_server_limited(signer)
            
        if from_vault.type == VAULT_TYPE.USER:
            return self.validate_signer_access_from_user(signer)

        return 'Validate logic not implemented for this vault type'
    
    def validate_signer_access_from_server_unlimited(self, signer: User) -> str | None:
        to_vault = self.to_vault

        if to_vault.type == VAULT_TYPE.SERVER_UNLIMITED:
            return 'Useless transfer'
        
        if signer.role == ROLE.ADMIN:
            return None
        
        if to_vault.type == VAULT_TYPE.USER and signer.user_id != to_vault.user_id:
            return "Can't transfer from server to other users"
        
        return None

    def validate_signer_access_from_server_limited(self, signer: User) -> str | None:
        if signer.role != ROLE.ADMIN:
            return 'Only a admin can transfer from server limited vaults'
        
        return None

    def validate_signer_access_from_user(self, signer: User) -> str | None:
        if signer.role != ROLE.ADMIN:
            if signer.user_id != self.from_vault.user_id:
                return "Can't transfer from other users vaults"
            
        return None
    
    def get_vaults(self) -> list[Vault]:
        return [ self.from_vault, self.to_vault ]