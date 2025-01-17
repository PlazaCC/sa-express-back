from typing import Any

from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User

from src.shared.wallet.tx_queues.base import TXBaseQueue
from src.shared.wallet.tx_results.push import TXPushResult

class TXServerSingleQueue(TXBaseQueue):
    tx_proc: Any

    def __init__(self, tx_proc: Any):
        self.tx_proc = tx_proc

    def vault_proc(self):
        return self.tx_proc.vault_proc

    async def push_tx(self, signer: User, tx: TX) -> TXPushResult:
        pass