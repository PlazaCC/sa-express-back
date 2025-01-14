from decimal import Decimal
from pydantic import BaseModel

from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.user import User

class Vault(BaseModel):
    type: VAULT_TYPE
    user_id: int | None
    balance: Decimal
    balanceLocked: Decimal
    locked: bool
    server_ref: str | None
    
    @staticmethod
    def from_dict_static(data: dict) -> 'Vault':
        return Vault(
            type=VAULT_TYPE[data['type']],
            user_id=data['user_id'] if 'user_id' in data else None,
            balance=Decimal(data['balance']),
            balanceLocked=Decimal(data['balanceLocked']),
            locked=data['locked'],
            server_ref=data['server_ref'] if 'server_ref' in data else None
        )

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'Vault':
        return Vault(
            type=VAULT_TYPE[data['type']],
            user_id=data['user_id'] if 'user_id' in data else None,
            balance=Decimal(0),
            balanceLocked=Decimal(0),
            locked=False,
            server_ref=data['server_ref'] if 'server_ref' in data else None
        )
    
    @staticmethod
    def from_tx_instr_snapshot(data: dict) -> 'Vault':
        return Vault.from_tx_snapshot(data)
    
    @staticmethod
    def init_server_unlimited() -> 'Vault':
        return Vault(
            type=VAULT_TYPE.SERVER_UNLIMITED,
            user_id=None,
            balance=Decimal(0),
            balanceLocked=Decimal(0),
            locked=False,
            server_ref=None
        )
    
    @staticmethod
    def default_config():
        return { 'balance': '0', 'balanceLocked': '0', 'locked': False }

    @staticmethod
    def from_user(user: User, config: dict = default_config()) -> 'Vault':
        return Vault(
            type=VAULT_TYPE.USER,
            user_id=user.user_id,
            balance=Decimal(config['balance']),
            balanceLocked=Decimal(config['balanceLocked']),
            locked=config['locked'],
            server_ref=None
        )
    
    @staticmethod
    def from_user_id(user_id: int, config: dict = default_config()) -> 'Vault':
        return Vault(
            type=VAULT_TYPE.USER,
            user_id=user_id,
            balance=Decimal(config['balance']),
            balanceLocked=Decimal(config['balanceLocked']),
            locked=config['locked'],
            server_ref=None
        )
    
    def to_dict(self) -> dict:
        result = {
            'type': self.type.value,
            'balance': str(self.balance),
            'balanceLocked': str(self.balanceLocked),
            'locked': self.locked
        }

        if self.user_id is not None:
            result['user_id'] = self.user_id

        if self.server_ref is not None:
            result['server_ref'] = self.server_ref
        
        return result
    
    def from_dict(self, data: dict) -> 'Vault':
        return Vault.from_dict_static(data)

    def to_tx_snapshot(self) -> dict:
        result = {
            'type': self.type.value,
        }

        if self.user_id is not None:
            result['user_id'] = self.user_id

        if self.server_ref is not None:
            result['server_ref'] = self.server_ref

        return result
    
    def to_tx_instr_snapshot(self) -> dict:
        return self.to_tx_snapshot()
    
    def to_identity_key(self) -> str:
        if self.type == VAULT_TYPE.SERVER_UNLIMITED:
            return 'SERVER_UNLIMITED'

        if self.type == VAULT_TYPE.SERVER_LIMITED:
            return 'SERVER_LIMITED_' + self.server_ref

        if self.type == VAULT_TYPE.USER:
            return 'USER_' + str(self.user_id)

        return 'UNKNOWN'

