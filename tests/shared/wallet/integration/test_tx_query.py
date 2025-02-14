import pytest
import random
import asyncio

from tests.shared.wallet.integration.common import load_app_env

load_app_env()

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.domain.entities.tx import TX

from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.decimal import Decimal, quantize
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.mocks.wallet_paygate_mock import WalletPayGateMock
from src.shared.wallet.tx_results.pop import TXPopResult
from src.shared.wallet.tx_results.push import TXPushResult
from src.shared.wallet.tx_templates.deposit import create_deposit_tx

pytest_plugins = ('pytest_asyncio')

class Test_TXQuery:
    ### UTILITY METHODS ###
    async def exec_tx(self, tx_proc: TXProcessor, signer: AuthAuthorizerDTO, tx: TX) -> None:
        paygate = tx_proc.paygate

        deferred = asyncio.get_event_loop().create_future()

        async def random_paygate_webhook():
            if len(paygate.pending_payments) == 0:
                return

            webhook_ref_header = paygate.pending_payments.pop()
            
            tx = tx_proc.get_tx_from_webhook(webhook_ref_header)

            assert tx is not None

            async def pop_callback(pop_result: TXPopResult):
                deferred.set_result(True)

                print(f'[{pop_result.timestamp}] TX pop')
            
            await tx_proc.pop_tx_with_callback(pop_callback, tx)

        async def push_callback(push_result: TXPushResult):
            print(f'[{push_result.timestamp}] TX push')

            if push_result.with_error():
                deferred.set_result(True)
                return

            await random_paygate_webhook()

        await tx_proc.push_tx_with_callback(push_callback, signer, tx)

        await deferred

    ### TEST METHODS ###
    # @pytest.mark.skip(reason='')
    @pytest.mark.asyncio
    async def test_query(self):
        base_repository = Repository(wallet_repo=True, wallet_cache=True)

        user = AuthAuthorizerDTO.from_api_gateway({
            'user_id': 0,
            'name': 'testuser',
            'email': 'testuser@gmail.com',
            'role': 'SUBAFILIADO',
            'email_verified': True
        })

        tx_proc = TXProcessor(
            cache=base_repository.wallet_cache,
            repository=base_repository.wallet_repo,
            paygate=WalletPayGateMock(),
            config=TXProcessorConfig(
                tx_queue_type=TX_QUEUE_TYPE.SERVER_SINGLE
            )
        )

        vault = tx_proc.vault_proc.create_if_not_exists(user)

        user_txs = base_repository.wallet_repo.get_transactions_by_user(user, ini_timestamp=1739537211403, \
            end_timestamp=1739537211708)

        txs = user_txs['txs']

        print('')
        for tx in txs:
            print(tx.tx_id, tx.create_timestamp)

        # if len(txs) == 0:
        #     for _ in range(0, 10):
        #         amount = quantize(Decimal(random.choice([ 10, 50, 100, 125, 150, 300 ])))
                
        #         tx = create_deposit_tx({ 'to_vault': vault, 'amount': amount })

        #         await self.exec_tx(tx_proc, user, tx)

        assert True


