from pydantic import BaseModel

from src.shared.domain.entities.vault import Vault
from src.shared.domain.enums.tx_status_enum import TX_STATUS

class TX(BaseModel):
    tx_id: int
    user_id: int
    timestamp: str
    vaults: list[Vault]
    instructions: list[object]
    logs: list[str]
    tx_status: TX_STATUS

    def to_dict(self):
        vault_dicts = [ v.to_dict() for v in self.vaults ]

        return {
            "tx_id": self.tx_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "vaults": vault_dicts,
            "instructions": self.instructions,
            "logs": self.logs,
            "tx_status": self.tx_status.value
        }
    
    def from_dict(self, data: dict) -> 'TX':
        vaults = [ Vault().from_dict(v) for v in data.vaults ]

        return TX(
            tx_id=data['tx_id'],
            user_id=data['user_id'],
            timestamp=data['timestamp'],
            vaults=vaults,
            instructions=data['instructions'],
            logs=data['logs'],
            tx_status=TX_STATUS[data['tx_status']]
        )