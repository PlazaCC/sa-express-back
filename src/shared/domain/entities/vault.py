from pydantic import BaseModel
from decimal import Decimal

from src.shared.domain.entities.user import User

class Vault(BaseModel):
    vault_id: int
    user_id: int
    balance: Decimal
    locked: bool

    @staticmethod
    def from_user(vault_id: int, user: User, config: object):
        balance = Decimal(config['balance']) if 'balance' in config else Decimal('0')
        locked = config['locked'] if 'locked' in config else False

        return Vault(
            vault_id=vault_id, 
            user_id=user.user_id, 
            balance=balance,
            locked=locked
        )
    
    def to_dict(self):
        return {
            "vault_id": self.vault_id,
            "user_id": self.user_id,
            "balance": self.balance,
            "locked": self.locked
        }
    
    def from_dict(self, data: dict) -> 'Vault':
        return Vault(
            vault_id=data['vault_id'],
            user_id=data['user_id'],
            balance=data['balance'],
            locked=data['locked']
        )
