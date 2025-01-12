from pydantic import BaseModel

from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.entities.vault import Vault
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.instructions.base import TXBaseInstruction
from src.shared.wallet.instructions.mutate import TXMutateInstruction

class TX(BaseModel):
    tx_id: str
    user_id: int
    timestamp: str
    vaults: list[Vault]
    instructions: list[TXBaseInstruction]
    logs: list[TXLogs]
    tx_status: TX_STATUS

    @staticmethod
    def from_dict_static(data: dict) -> 'TX':
        return TX(
            tx_id=data['tx_id'],
            user_id=data['user_id'],
            timestamp=data['timestamp'],
            vaults=[ Vault.from_tx_snapshot(v) for v in data['vaults'] ],
            instructions=[ TXMutateInstruction.from_tx_snapshot(i) for i in data['instructions'] ],
            logs=[ TXLogs.from_tx_snapshot(l) for l in data['logs'] ],
            tx_status=TX_STATUS[data['tx_status']]
        )
    
    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TX':
        return TX.from_dict_static(data)

    def to_dict(self) -> dict:
        return {
            'tx_id': self.tx_id,
            'user_id': self.user_id,
            'timestamp': self.timestamp,
            'vaults': [ v.to_tx_snapshot() for v in self.vaults ],
            'instructions': [ i.to_tx_snapshot() for i in self.instructions ],
            'logs': [ l.to_tx_snapshot() for l in self.logs ],
            'tx_status': self.tx_status.value
        }
    
    def from_dict(self, data: dict) -> 'TX':
        return TX.from_dict_static(data)

    def to_tx_snapshot(self) -> object:
        return self.to_dict()