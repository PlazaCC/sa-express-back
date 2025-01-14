import uuid
from pydantic import BaseModel, ConfigDict

from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.instructions.base import TXBaseInstruction
from src.shared.wallet.instructions.mutate import TXMutateInstruction

class TX(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tx_id: str
    user_id: int
    create_timestamp: str
    sign_timestamp: str | None
    commit_timestamp: str | None
    vaults: list[Vault]
    instructions: list[TXBaseInstruction]
    logs: list[TXLogs]
    status: TX_STATUS

    @staticmethod
    def from_dict_static(data: dict) -> 'TX':
        return TX(
            tx_id=data['tx_id'],
            user_id=data['user_id'],
            create_timestamp=data['create_timestamp'],
            sign_timestamp=data['sign_timestamp'] if 'sign_timestamp' in data else None,
            commit_timestamp=data['commit_timestamp'] if 'commit_timestamp' in data else None,
            vaults=[ Vault.from_tx_snapshot(v) for v in data['vaults'] ],
            instructions=[ TXMutateInstruction.from_tx_snapshot(i) for i in data['instructions'] ],
            logs=[ TXLogs.from_tx_snapshot(l) for l in data['logs'] ],
            status=TX_STATUS[data['tx_status']]
        )
    
    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TX':
        return TX.from_dict_static(data)
    
    @staticmethod
    def random_id():
        return str(uuid.uuid4())

    def to_dict(self) -> dict:
        result = {
            'tx_id': self.tx_id,
            'user_id': self.user_id,
            'create_timestamp': self.create_timestamp,
            'vaults': [ v.to_tx_snapshot() for v in self.vaults ],
            'instructions': [ i.to_tx_snapshot() for i in self.instructions ],
            'logs': [ l.to_tx_snapshot() for l in self.logs ],
            'status': self.status.value
        }

        if self.sign_timestamp is not None:
            result['sign_timestamp'] = self.sign_timestamp

        if self.commit_timestamp is not None:
            result['commit_timestamp'] = self.commit_timestamp

        return result
    
    def from_dict(self, data: dict) -> 'TX':
        return TX.from_dict_static(data)

    def to_tx_snapshot(self) -> dict:
        return self.to_dict()