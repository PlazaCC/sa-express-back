from decimal import Decimal

from src.shared.domain.entities.vault import Vault
from src.shared.wallet.instructions.base import TXBaseInstruction, TX_INSTRUCTION_TYPE

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