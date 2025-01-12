from pydantic import BaseModel
from decimal import Decimal

from src.shared.domain.entities.user import User

class Vault(BaseModel):
    user_id: int
    balance: Decimal
    locked: bool

    @staticmethod
    def from_user(user: User, config: object):
        balance = Decimal(config['balance']) if 'balance' in config else Decimal('0')
        locked = config['locked'] if 'locked' in config else False

        return Vault(
            user_id=user.user_id, 
            balance=balance,
            locked=locked
        )
    
    @staticmethod
    def from_dict_static(data):
        return Vault(
            user_id=data['user_id'],
            balance=Decimal(data['balance']),
            locked=data['locked']
        )
    
    @staticmethod
    def from_tx_snapshot(data: dict) -> 'Vault':
        return Vault(
            user_id=data['user_id'],
            balance=Decimal(data['balance']),
            locked=False
        )
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "balance": str(self.balance),
            "locked": self.locked
        }
    
    def from_dict(self, data: dict) -> 'Vault':
        return Vault(
            user_id=data['user_id'],
            balance=Decimal(data['balance']),
            locked=data['locked']
        )
    
    def to_tx_snapshot(self):
        return {
            "user_id": self.user_id,
            "balance": str(self.balance)
        }
