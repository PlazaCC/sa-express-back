from decimal import Decimal

from src.shared.domain.entities.vault import Vault

class TXTransferInstruction:
    from_vault: int
    to_vault: int
    amount: Decimal

    def __init__(self, from_vault: int, to_vault: int, amount: Decimal):
        self.from_vault = from_vault
        self.to_vault = to_vault
        self.amount = amount

    def to_tx_snapshot(self):
        return {
            'from_vault': self.from_vault,
            'to_vault': self.to_vault,
            'amount': str(self.amount),
        }