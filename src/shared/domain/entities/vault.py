from pydantic import BaseModel, ConfigDict

from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.dtos.user_api_gateway_dto import UserApiGatewayDTO

from src.shared.wallet.decimal import Decimal
from src.shared.wallet.models.pix import PIXKey

class Vault(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: VAULT_TYPE
    user_id: int | None
    server_ref: str | None
    balance: Decimal
    balance_locked: Decimal
    locked: bool
    pix_key: PIXKey | None
    
    @staticmethod
    def from_dict_static(data: dict) -> 'Vault':
        return Vault(
            type=VAULT_TYPE[data['type']],
            user_id=int(data['user_id']) if 'user_id' in data else None,
            server_ref=data['server_ref'] if 'server_ref' in data else None,
            balance=Decimal(data['balance']),
            balance_locked=Decimal(data['balance_locked']),
            locked=data['locked'],
            pix_key=PIXKey.from_dict_static(data['pix_key']) if 'pix_key' in data else None
        )

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'Vault':
        return Vault(
            type=VAULT_TYPE[data['type']],
            user_id=int(data['user_id']) if 'user_id' in data else None,
            server_ref=data['server_ref'] if 'server_ref' in data else None,
            balance=Decimal(0),
            balance_locked=Decimal(0),
            locked=False,
            pix_key=None
        )
    
    @staticmethod
    def from_tx_instr_snapshot(data: dict) -> 'Vault':
        return Vault.from_tx_snapshot(data)
    
    @staticmethod
    def init_server_unlimited() -> 'Vault':
        return Vault(
            type=VAULT_TYPE.SERVER_UNLIMITED,
            user_id=None,
            server_ref=None,
            balance=Decimal(0),
            balance_locked=Decimal(0),
            locked=False,
            pix_key=None
        )
    
    @staticmethod
    def default_config():
        return { 'balance': '0', 'balance_locked': '0', 'locked': False }

    @staticmethod
    def from_user(user: User | UserApiGatewayDTO, config: dict = default_config()) -> 'Vault':
        return Vault(
            type=VAULT_TYPE.USER,
            user_id=int(user.user_id),
            server_ref=None,
            balance=Decimal(config['balance']),
            balance_locked=Decimal(config['balance_locked']),
            locked=config['locked'],
            pix_key=None
        )
    
    @staticmethod
    def from_user_id(user_id: int | str, config: dict = default_config()) -> 'Vault':
        return Vault(
            type=VAULT_TYPE.USER,
            user_id=int(user_id),
            server_ref=None,
            balance=Decimal(config['balance']),
            balance_locked=Decimal(config['balance_locked']),
            locked=config['locked'],
            pix_key=None
        )
    
    @staticmethod
    def get_tx_execution_state_total_balance(state: dict) -> Decimal:
        return state['balance'] - state['balance_locked']
    
    @staticmethod
    def user_id_to_identity_key(user_id: int) -> str:
        return 'USER_' + str(user_id)
    
    @staticmethod
    def server_ref_to_identity_key(server_ref: str) -> str:
        return 'SERVER_LIMITED_' + server_ref

    def to_dict(self) -> dict:
        result = {
            'type': self.type.value,
            'balance': str(self.balance),
            'balance_locked': str(self.balance_locked),
            'locked': self.locked
        }

        if self.user_id is not None:
            result['user_id'] = self.user_id

        if self.server_ref is not None:
            result['server_ref'] = self.server_ref

        if self.pix_key is not None:
            result['pix_key'] = self.pix_key.to_dict()

        result['partition_key'] = self.to_identity_key()
        
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
    
    def to_tx_execution_state(self) -> tuple[str, dict]:
        state = {
            'balance': Decimal(self.balance),
            'balance_locked': Decimal(self.balance_locked),
        }

        return self.to_identity_key(), state

    def total_balance(self):
        return self.balance - self.balance_locked
    
    def update_state(self, next_state: dict) -> None:
        self.balance = next_state['balance']
        self.balance_locked = next_state['balance_locked']

    def __eq__(self, other: 'Vault') -> bool:
        return self.to_identity_key() == other.to_identity_key()
    
    def __hash__(self) -> int:
        return hash(self.to_identity_key())
    
    def to_user_public(self) -> dict:
        result = {}

        if self.pix_key is not None:
            result['pix_key'] = self.pix_key.to_dict()

        result['total_balance'] = str(self.total_balance())
        result['balance_locked'] = str(self.balance_locked)
        
        return result