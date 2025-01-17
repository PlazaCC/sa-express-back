from typing import Any

from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User

from src.shared.wallet.tx_queues.base import TXBaseQueue
from src.shared.wallet.tx_results.push import TXPushResult

class TXClientQueue(TXBaseQueue):
    tx_proc: Any

    def __init__(self, tx_proc: Any):
        self.tx_proc = tx_proc

    def vault_proc(self):
        return self.tx_proc.vault_proc

    async def push_tx(self, signer: User, tx: TX) -> TXPushResult:
        vault_res = await self.vault_proc().get_and_lock(tx.vaults)

        if vault_res is None:
            return TXPushResult.locked()

        tx.vaults = vault_res

        sign_result = await self.tx_proc.sign(signer, tx)
        
        # TODO: handle real cache errors
        await self.vault_proc().unlock(tx.vaults)

        return TXPushResult.successful(sign_result)