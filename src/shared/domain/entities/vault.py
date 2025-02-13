from pydantic import BaseModel, ConfigDict

from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.wallet.enums.pix import PIX_KEY_TYPE
from src.shared.wallet.decimal import Decimal
from src.shared.wallet.models.pix import PIXKey

class Vault(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    type: VAULT_TYPE
    user_id: int | None
    balance: Decimal
    balance_locked: Decimal
    pix_key: PIXKey | None
    
    @staticmethod
    def from_dict_static(data: dict) -> 'Vault':
        pix_key = None

        if 'pix_key' in data:
            pix_key = PIXKey.from_dict_static(data['pix_key'])
        elif 'pix_key_type' in data:
            pix_key = PIXKey(
                type=PIX_KEY_TYPE[data['pix_key_type']],
                value=data['pix_key_value']
            )

        return Vault(
            type=VAULT_TYPE[data['type']],
            user_id=int(data['user_id']) if 'user_id' in data else None,
            balance=Decimal(data['balance']),
            balance_locked=Decimal(data['balance_locked']),
            pix_key=pix_key
        )

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'Vault':
        return Vault(
            type=VAULT_TYPE[data['type']],
            user_id=int(data['user_id']) if 'user_id' in data else None,
            balance=Decimal(data['balance']),
            balance_locked=Decimal(data['balance_locked']),
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
            balance=Decimal(0),
            balance_locked=Decimal(0),
            pix_key=None
        )
    
    @staticmethod
    def default_config():
        return { 'balance': '0', 'balance_locked': '0' }

    @staticmethod
    def from_user(user: User | AuthAuthorizerDTO, config: dict = default_config()) -> 'Vault':
        return Vault(
            type=VAULT_TYPE.USER,
            user_id=int(user.user_id),
            balance=Decimal(config['balance']),
            balance_locked=Decimal(config['balance_locked']),
            pix_key=None
        )
    
    @staticmethod
    def from_user_id(user_id: int | str, config: dict = default_config()) -> 'Vault':
        return Vault(
            type=VAULT_TYPE.USER,
            user_id=int(user_id),
            balance=Decimal(config['balance']),
            balance_locked=Decimal(config['balance_locked']),
            pix_key=None
        )
    
    @staticmethod
    def get_tx_execution_state_total_balance(state: dict) -> Decimal:
        return state['balance'] - state['balance_locked']
    
    @staticmethod
    def user_id_to_identity_key(user_id: int) -> str:
        return 'USER_' + str(user_id)
    
    @staticmethod
    def from_redis_hgetall(data: dict) -> 'Vault':
        user_id = None if data[b'user_id'] == b'' else data[b'user_id'].decode('utf8')
        balance = Decimal(data[b'balance'].decode('utf8'))
        balance_locked = Decimal(data[b'balance_locked'].decode('utf8'))
        
        pix_key = None

        if data[b'pix_key_type'] != b'':
            pix_key = PIXKey(
                type=PIX_KEY_TYPE[data[b'pix_key_type'].decode('utf8')],
                value=data[b'pix_key_value'].decode('utf8')
            )

        return Vault(
            type=VAULT_TYPE.USER,
            user_id=user_id,
            balance=balance,
            balance_locked=balance_locked,
            pix_key=pix_key
        )
    
    @staticmethod
    def from_redis_hgetall_list(data: list) -> 'Vault':
        data_dict = {}

        for i in range(0, len(data), 2):
            data_dict[data[i]] = data[i + 1]

        return Vault.from_redis_hgetall(data_dict)

    def to_dict(self, dynamodb=False) -> dict:
        result = {
            'type': self.type.value,
            'balance': str(self.balance),
            'balance_locked': str(self.balance_locked)
        }

        if self.user_id is not None:
            result['user_id'] = self.user_id
        
        if self.pix_key is not None:
            if dynamodb:
                result['pix_key_type'] = self.pix_key.type.value
                result['pix_key_value'] = self.pix_key.value
            else:
                result['pix_key'] = self.pix_key.to_dict()
        
        return result
    
    def from_dict(self, data: dict) -> 'Vault':
        return Vault.from_dict_static(data)

    def to_tx_snapshot(self) -> dict:
        result = {
            'type': self.type.value,
            'balance': str(self.balance),
            'balance_locked': str(self.balance_locked)
        }
        
        if self.user_id is not None:
            result['user_id'] = self.user_id

        return result
    
    def to_tx_instr_snapshot(self) -> dict:
        return self.to_tx_snapshot()
    
    def to_identity_key(self) -> str:
        if self.type == VAULT_TYPE.SERVER_UNLIMITED:
            return 'SERVER_UNLIMITED'

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
    
    def to_redis_upsert_args(self) -> list[str]:
        vault_id_key = self.to_identity_key()

        return [ 
            vault_id_key,
            str(self.balance),
            str(self.balance_locked),
            '' if self.user_id is None else str(self.user_id),
            '' if self.pix_key is None else self.pix_key.type.value,
            '' if self.pix_key is None else self.pix_key.value
        ]
    
    def lockable(self) -> bool:
        if self.type == VAULT_TYPE.SERVER_UNLIMITED:
            return False
        
        return True