from decimal import Decimal

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault

from src.shared.wallet.enums.tx_instruction_type import TX_INSTRUCTION_TYPE
from src.shared.wallet.tx_instructions.base import TXBaseInstruction
from src.shared.wallet.tx_instruction_results.transfer import TXTransferInstructionResult
from src.shared.wallet.tx_promises.pix_deposit import TXPIXDepositPromise
from src.shared.wallet.tx_promises.pix_withdrawal import TXPIXWithdrawalPromise

class TXTransferInstruction(TXBaseInstruction):
    from_vault: Vault
    to_vault: Vault
    amount: Decimal

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXTransferInstruction':
        return TXTransferInstruction(
            from_vault=Vault.from_tx_instr_snapshot(data['from_vault']),
            to_vault=Vault.from_tx_instr_snapshot(data['to_vault']),
            amount=Decimal(data['amount'])
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
    
    def validate_fields_before_sign(self) -> str | None:
        amount = self.amount

        if amount == 0:
            return "Can't transfer zero amount"
        
        if amount < 0 :
            return "Can't transfer negative amount"
        
        from_vault = self.from_vault

        if from_vault.type == VAULT_TYPE.SERVER_UNLIMITED:
            return None

        if amount > from_vault.total_balance():
            return 'Amount is greater than vault balance'
        
        return None
    
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
    
    def update_vaults(self, vaults: list[Vault]) -> None:
        self.update_vault('from_vault', vaults)
        self.update_vault('to_vault', vaults)

    def update_vault(self, field_key: str, vaults: list[Vault]) -> None:
        vault_field = getattr(self, field_key)

        vault_key = vault_field.to_identity_key()

        next_vault = next((v for v in vaults if v.to_identity_key() == vault_key), None)

        if next_vault is not None:
            vault_field = next_vault

    def is_deposit(self) -> bool:
        return self.from_vault.type == VAULT_TYPE.SERVER_UNLIMITED and self.to_vault.type == VAULT_TYPE.USER
    
    def is_withdrawal(self) -> bool:
        return self.from_vault.type == VAULT_TYPE.USER and self.to_vault.type == VAULT_TYPE.SERVER_UNLIMITED

    async def execute(self, instr_index: int, state: dict, from_sign: bool) -> tuple[dict, TXTransferInstructionResult]:
        from_vault = self.from_vault
        to_vault = self.to_vault

        from_vault_key = from_vault.to_identity_key()
        to_vault_key = to_vault.to_identity_key()

        if from_vault.type != VAULT_TYPE.SERVER_UNLIMITED:
            from_vault_state = state['vaults'][from_vault_key]
            
            if self.is_withdrawal():
                if from_sign:
                    from_vault_state['balance_locked'] += self.amount
                else:
                    from_vault_state['balance_locked'] -= self.amount
                    from_vault_state['balance'] -= self.amount
            else:
                from_vault_state['balance'] -= self.amount

            if Vault.get_tx_execution_state_total_balance(from_vault_state) < 0:
                return state, TXTransferInstructionResult.failed(f'Amount too low on vault "{from_vault_key}"')
            
        if to_vault.type != VAULT_TYPE.SERVER_UNLIMITED:
            to_vault_state = state['vaults'][to_vault_key]

            to_vault_state['balance'] += self.amount

        if from_sign and self.is_deposit():
            deposit_pix_key = to_vault.pix_key

            if deposit_pix_key is None:
                return state, TXTransferInstructionResult.failed(f"PIX key isn't defined for vault \"{to_vault_key}\"")

            return state, TXTransferInstructionResult.successful(
                TXPIXDepositPromise(
                    tx_id=state['tx_id'],
                    instr_index=instr_index,
                    pix_key=to_vault.pix_key, 
                    amount=self.amount
                )
            )
        
        if from_sign and self.is_withdrawal():
            withdrawal_pix_key = from_vault.pix_key

            if withdrawal_pix_key is None:
                return state, TXTransferInstructionResult.failed(f"PIX key isn't defined for vault \"{from_vault_key}\"")

            return state, TXTransferInstructionResult.successful([ 
                TXPIXWithdrawalPromise(
                    tx_id=state['tx_id'],
                    instr_index=instr_index,
                    pix_key=from_vault.pix_key, 
                    amount=self.amount
                )
            ])

        return state, TXTransferInstructionResult.successful()
    
    async def revert(self, instr_index: int, state: dict) -> tuple[dict, TXTransferInstructionResult]:
        from_vault = self.from_vault
        to_vault = self.to_vault

        from_vault_key = from_vault.to_identity_key()
        to_vault_key = to_vault.to_identity_key()

        if from_vault.type != VAULT_TYPE.SERVER_UNLIMITED:
            from_vault_state = state['vaults'][from_vault_key]

            if self.is_withdrawal():
                from_vault_state['balance_locked'] -= self.amount
            else:
                from_vault_state['balance'] += self.amount

        if to_vault.type != VAULT_TYPE.SERVER_UNLIMITED:
            to_vault_state = state['vaults'][to_vault_key]

            to_vault_state['balance'] -= self.amount

        return state, TXTransferInstructionResult.successful()