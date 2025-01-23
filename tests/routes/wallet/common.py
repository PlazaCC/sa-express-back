from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.domain.entities.tx import TX
from src.shared.infra.repositories.mocks.wallet_cache_mock import WalletCacheMock
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock

from src.shared.wallet.enums.pix import PIX_KEY_TYPE
from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.mocks.wallet_paygate_mock import WalletPayGateMock
from src.shared.wallet.tx_results.push import TXPushResult
from src.shared.wallet.tx_results.pop import TXPopResult
from src.shared.wallet.tx_templates.deposit import create_deposit_tx
from src.shared.wallet.tx_templates.withdrawal import create_withdrawal_tx

from tests.shared.wallet.mocks.common import get_back_context

def initialize_mocks() -> tuple[WalletCacheMock, WalletRepositoryMock, WalletPayGateMock]:
    (cache, repository, paygate) = get_back_context({
        'num_users': 2,
        'user_status': [ USER_STATUS.CONFIRMED.value ],
        'create_vaults': {
            'random_balance': True,
            'locked': False
        },
        'singleton': True
    })

    for vault in repository.get_all_user_vaults():
        vault.pix_key = PIXKey(PIX_KEY_TYPE.CPF, '85223578970')

        cache.upsert_vault(vault)
        repository.create_vault(vault)

    return (cache, repository, paygate)

async def deposit_mock(cache: WalletCacheMock, repository: WalletRepositoryMock, \
    paygate: WalletPayGateMock) -> tuple[TX, TXPushResult]:
    tx_proc = TXProcessor(cache, repository, paygate, 
        config=TXProcessorConfig(
            max_vaults=2,
            max_instructions=1,
            tx_queue_type=TX_QUEUE_TYPE.CLIENT
        )
    )

    vault = repository.get_random_vault()
    signer = repository.get_user_by_user_id(vault.user_id)

    tx = create_deposit_tx({ 'to_vault': vault, 'amount': '150' })

    push_result = await tx_proc.push_tx(signer, tx)

    return (tx, push_result)

async def withdrawal_mock(cache: WalletCacheMock, repository: WalletRepositoryMock, \
    paygate: WalletPayGateMock) -> tuple[TX, TXPopResult]:
    tx_proc = TXProcessor(cache, repository, paygate,
        config=TXProcessorConfig(
            max_vaults=2,
            max_instructions=1,
            tx_queue_type=TX_QUEUE_TYPE.CLIENT
        )
    )
    
    vault = repository.get_random_vault()
    signer = repository.get_user_by_user_id(vault.user_id)

    tx = create_withdrawal_tx({ 'from_vault': vault, 'amount': '150' })

    pop_result = await tx_proc.push_tx(signer, tx)

    return (tx, pop_result)