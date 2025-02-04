from typing import Any

from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.wallet.tx_queues.base import TXBaseQueue
from src.shared.wallet.tx_results.push import TXPushResult
from src.shared.wallet.tx_results.pop import TXPopResult

class TXServerMultiQueue(TXBaseQueue):
    tx_proc: Any

    def __init__(self, tx_proc: Any):
        self.tx_proc = tx_proc

    def vault_proc(self):
        pass

    async def push_tx(self, signer: User | AuthAuthorizerDTO, tx: TX) -> TXPushResult:
        pass

    async def pop_tx(self, tx: TX, error: str | None = None) -> TXPopResult:
        pass