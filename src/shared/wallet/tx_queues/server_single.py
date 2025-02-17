import asyncio
from typing import Any, Awaitable
from collections.abc import Callable

from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.wallet.tx_queues.base import TXBaseQueue
from src.shared.wallet.tx_results.push import TXPushResult
from src.shared.wallet.tx_results.pop import TXPopResult

class TXServerSingleQueue(TXBaseQueue):
    tx_proc: Any

    def __init__(self, tx_proc: Any):
        self.tx_proc = tx_proc

    def vault_proc(self):
        return self.tx_proc.vault_proc

    async def _push_tx(self, signer: User | AuthAuthorizerDTO, tx: TX) -> TXPushResult:
        locked_vaults = self.vault_proc().get_and_lock(tx.instruction.get_vaults())

        if locked_vaults is None:
            return TXPushResult.locked()

        tx.instruction.update_vaults(locked_vaults)

        sign_result = await self.tx_proc.sign(signer, tx)

        self.vault_proc().unlock(tx.instruction.get_vaults())

        return TXPushResult.successful(sign_result)

    async def push_tx(self, callback: Callable[[], Awaitable[TXPushResult]], signer: User, tx: TX) -> None:
        push_result = await self._push_tx(signer, tx)

        if push_result.error == 'Locked':
            async def next_push():
                await asyncio.sleep(0.01)
                await self.push_tx(callback, signer, tx)

            asyncio.ensure_future(next_push())
            return

        await callback(push_result)
    
    async def _pop_tx(self, tx: TX, error: str | None = None) -> TXPopResult:
        locked_vaults = self.vault_proc().get_and_lock(tx.instruction.get_vaults())

        if locked_vaults is None:
            return TXPopResult.locked()
        
        tx.instruction.update_vaults(locked_vaults)

        if error is None:
            commit_result = await self.tx_proc.commit_tx_confirmed(tx)
        else:
            commit_result = await self.tx_proc.commit_tx_failed(tx, error)

        self.vault_proc().unlock(tx.instruction.get_vaults())

        return TXPopResult.successful(commit_result)

    async def pop_tx(self, callback: Callable[[], Awaitable[TXPopResult]], tx: TX, \
        error: str | None = None) -> None:
        pop_result = await self._pop_tx(tx, error)

        if pop_result.error == 'Locked':
            async def next_pop():
                await asyncio.sleep(0.01)
                await self.pop_tx(callback, tx, error)

            asyncio.ensure_future(next_pop())
            return

        await callback(pop_result)