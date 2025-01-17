import asyncio
from typing import Any, Awaitable
from collections.abc import Callable

from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User

from src.shared.wallet.tx_queues.base import TXBaseQueue
from src.shared.wallet.tx_results.push import TXPushResult
from src.shared.wallet.tx_results.pop import TXPopResult

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
    
    async def _pop_tx(self, tx: TX, instr_index: int, error: str | None = None) -> TXPopResult:
        vault_res = await self.vault_proc().get_and_lock(tx.vaults)

        if vault_res is None:
            return TXPopResult.failed('Locked')
        
        tx.vaults = vault_res

        if error is None:
            commit_result = await self.tx_proc.commit_tx_confirmed(tx, instr_index)
        else:
            commit_result = await self.tx_proc.commit_tx_failed(tx, instr_index, error)

        # TODO: handle real cache errors
        await self.vault_proc().unlock(tx.vaults)

        return TXPopResult.successful(commit_result)

    async def pop_tx(self, callback: Callable[[], Awaitable[TXPopResult]], \
        tx: TX, instr_index: int, error: str | None = None) -> None:
        pop_result = await self._pop_tx(tx, instr_index, error)

        if pop_result.error == 'Locked':
            async def next_pop():
                await asyncio.sleep(0.01)
                await self.pop_tx(callback, tx, instr_index, error)

            asyncio.ensure_future(next_pop())
            return

        await callback(pop_result)