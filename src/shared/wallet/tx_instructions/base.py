from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.infra.repositories.dtos.user_api_gateway_dto import UserApiGatewayDTO

from src.shared.wallet.tx_instruction_results.base import TXBaseInstructionResult

class TXBaseInstruction:
    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXBaseInstruction':
        pass

    def __init__(self):
        pass

    def to_tx_snapshot(self) -> dict:
        pass
    
    def validate_fields_before_sign(self) -> str | None:
        pass
    
    def validate_signer_access(self, user: User | UserApiGatewayDTO) -> str | None:
        pass
    
    def get_vaults(self) -> list[Vault]:
        pass

    def update_vaults(self, vaults: list[Vault]) -> None:
        pass

    def update_vault(self, field_key: str, vaults: list[Vault]) -> None:
        pass

    async def execute(self, instr_index: int, state: dict) -> tuple[dict, TXBaseInstructionResult]:
        pass

    async def revert(self, instr_index: int, state: dict) -> tuple[dict, TXBaseInstructionResult]:
        pass

