from src.shared.wallet.instructions.transfer import TXTransferInstruction

from src.shared.wallet.instructions.base import TX_INSTRUCTION_TYPE

class TXMutateInstruction:
    @staticmethod
    def from_tx_snapshot(data: dict):
        if data['type'] == TX_INSTRUCTION_TYPE.TRANSFER.value:
            return TXTransferInstruction.from_tx_snapshot(data)

        return None
        