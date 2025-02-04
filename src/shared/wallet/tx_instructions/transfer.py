from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.wallet.decimal import Decimal, quantize
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
        
        self.set_amount(amount)

    def set_amount(self, amount: Decimal):
        self.amount = quantize(amount)

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
            return 'Não é possível transferir valor nulo'
        
        if amount < 0:
            return 'Não é possível transferir valor negativo'
        
        from_vault = self.from_vault
        to_vault = self.to_vault

        if from_vault.to_identity_key() == to_vault.to_identity_key():
            return 'Transferência não teria efeito nenhum'

        if from_vault.type == VAULT_TYPE.SERVER_UNLIMITED:
            return None

        if amount > from_vault.total_balance():
            return 'Valor é maior que o saldo do remetente'
        
        return None
    
    def validate_signer_access(self, signer: User | AuthAuthorizerDTO) -> str | None:
        from_vault = self.from_vault

        if from_vault.type == VAULT_TYPE.SERVER_UNLIMITED:
            return self.validate_signer_access_from_server_unlimited(signer)
            
        if from_vault.type == VAULT_TYPE.USER:
            return self.validate_signer_access_from_user(signer)

        return f'Validação de assinante ainda não foi implementada para o tipo de vault "{from_vault.type.value}"'
    
    def validate_signer_access_from_server_unlimited(self, signer: User | AuthAuthorizerDTO) -> str | None:
        to_vault = self.to_vault

        if to_vault.type == VAULT_TYPE.SERVER_UNLIMITED:
            return 'Transferência não teria efeito nenhum'
        
        if signer.role == ROLE.ADMIN:
            return None
        
        if to_vault.type == VAULT_TYPE.USER and signer.user_id != to_vault.user_id:
            return 'Não é permitido transferir do servidor para terceiros'
        
        return None

    def validate_signer_access_from_user(self, signer: User | AuthAuthorizerDTO) -> str | None:
        if signer.role != ROLE.ADMIN:
            if signer.user_id != self.from_vault.user_id:
                return 'Não é permitido transferir saldo de terceiros'
            
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
            setattr(self, field_key, next_vault)

    def is_deposit(self) -> bool:
        return self.from_vault.type == VAULT_TYPE.SERVER_UNLIMITED and self.to_vault.type == VAULT_TYPE.USER
    
    def is_withdrawal(self) -> bool:
        return self.from_vault.type == VAULT_TYPE.USER and self.to_vault.type == VAULT_TYPE.SERVER_UNLIMITED
    
    def get_ref_id(self) -> str:
        vault_ids = [ self.from_vault.to_identity_key(), self.to_vault.to_identity_key() ]

        vault_ids.sort()

        return ':'.join(vault_ids)
    
    async def execute(self, state: dict, from_sign: bool) -> tuple[dict, TXTransferInstructionResult]:
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
                return state, TXTransferInstructionResult.failed(f'Remetente não possui saldo suficiente')
            
        if to_vault.type != VAULT_TYPE.SERVER_UNLIMITED:
            to_vault_state = state['vaults'][to_vault_key]

            to_vault_state['balance'] += self.amount

        if from_sign and self.is_deposit():
            return state, TXTransferInstructionResult.successful(
                TXPIXDepositPromise(
                    tx_id=state['tx_id'],
                    nonce=state['nonce'],
                    amount=self.amount,
                    ref_id=self.get_ref_id()
                )
            )
        
        if from_sign and self.is_withdrawal():
            withdrawal_pix_key = from_vault.pix_key

            if withdrawal_pix_key is None:
                return state, TXTransferInstructionResult.failed('Remetente não possui uma chave PIX')

            return state, TXTransferInstructionResult.successful(
                TXPIXWithdrawalPromise(
                    tx_id=state['tx_id'],
                    nonce=state['nonce'],
                    pix_key=from_vault.pix_key, 
                    amount=self.amount,
                    ref_id=self.get_ref_id()
                )
            )

        return state, TXTransferInstructionResult.successful()
    
    async def revert(self, state: dict) -> tuple[dict, TXTransferInstructionResult]:
        from_vault = self.from_vault

        from_vault_key = from_vault.to_identity_key()

        if from_vault.type != VAULT_TYPE.SERVER_UNLIMITED:
            from_vault_state = state['vaults'][from_vault_key]

            if self.is_withdrawal():
                from_vault_state['balance_locked'] -= self.amount

        return state, TXTransferInstructionResult.successful()