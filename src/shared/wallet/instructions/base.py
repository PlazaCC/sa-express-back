from src.shared.domain.entities.user import User

class TXBaseInstruction:
    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXBaseInstruction':
        pass

    def __init__(self):
        pass

    def to_tx_snapshot(self) -> dict:
        pass

    def validate_signer_access(self, user: User) -> str | None:
        pass