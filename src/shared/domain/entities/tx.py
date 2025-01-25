import uuid
from pydantic import BaseModel, ConfigDict

from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.entities.vault import Vault
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_instructions.base import TXBaseInstruction
from src.shared.wallet.tx_instructions.mutate import TXMutateInstruction
from src.shared.wallet.tx_results.sign import TXSignResult
from src.shared.wallet.tx_results.commit import TXCommitResult

class TX(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tx_id: str
    user_id: int
    create_timestamp: str
    vaults: list[Vault]
    instruction: TXBaseInstruction
    logs: TXLogs | None
    status: TX_STATUS
    sign_result: TXSignResult | None
    commit_result: TXCommitResult | None

    @staticmethod
    def from_dict_static(data: dict) -> 'TX':
        return TX(
            tx_id=data['tx_id'],
            user_id=data['user_id'],
            create_timestamp=data['create_timestamp'],
            vaults=[ Vault.from_tx_snapshot(v) for v in data['vaults'] ],
            instruction=TXMutateInstruction.from_tx_snapshot(data['instruction']),
            logs=TXLogs.from_tx_snapshot(data['logs']) if 'logs' in data else None,
            status=TX_STATUS[data['status']],
            sign_result=TXSignResult.from_tx_snapshot(data['sign_result']) if 'sign_result' in data else None,
            commit_result=TXCommitResult.from_tx_snapshot(data['commit_result']) if 'commit_result' in data else None
        )
    
    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TX':
        return TX.from_dict_static(data)
    
    @staticmethod
    def random_id():
        return str(uuid.uuid4())

    @staticmethod
    def invalid_tx_id(tx_id: str) -> bool:
        try:
            uuid.UUID(tx_id, version=4)
        except:
            return True

        return False

    def to_dict(self) -> dict:
        result = {
            'tx_id': self.tx_id,
            'user_id': self.user_id,
            'create_timestamp': self.create_timestamp,
            'vaults': [ v.to_tx_snapshot() for v in self.vaults ],
            'instruction': self.instruction.to_tx_snapshot(),
            'status': self.status.value,
        }

        if self.logs is not None:
            result['logs'] = self.logs.to_tx_snapshot()
        
        if self.sign_result is not None:
            result['sign_result'] = self.sign_result.to_tx_snapshot()

        if self.commit_result is not None:
            result['commit_result'] = self.commit_result.to_tx_snapshot()

        return result
    
    def from_dict(self, data: dict) -> 'TX':
        return TX.from_dict_static(data)

    def to_tx_snapshot(self) -> dict:
        return self.to_dict()