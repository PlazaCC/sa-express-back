from src.shared.wallet.enums.tx_instruction_type import TX_INSTRUCTION_TYPE
from src.shared.wallet.tx_instructions.transfer import TXTransferInstruction

class TXMutateInstruction:
    @staticmethod
    def from_tx_snapshot(data: dict):
        if data['type'] == TX_INSTRUCTION_TYPE.TRANSFER.value:
            return TXTransferInstruction.from_tx_snapshot(data)

        return None
        