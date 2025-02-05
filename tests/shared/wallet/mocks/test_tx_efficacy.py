import pytest
import random
import asyncio

from tests.shared.wallet.mocks.common import load_app_env, get_back_context

load_app_env()

from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.mocks.wallet_cache_mock import WalletCacheMock
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock

from src.shared.wallet.decimal import Decimal, quantize
from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.tx_results.pop import TXPopResult
from src.shared.wallet.tx_results.push import TXPushResult
from src.shared.wallet.tx_templates.deposit import create_deposit_tx
from src.shared.wallet.tx_templates.withdrawal import create_withdrawal_tx

pytest_plugins = ('pytest_asyncio')

class Test_TXEfficacy:
    ### UTILITY METHODS ###
    async def get_random_tx_batch(self, cache: WalletCacheMock, repository: WalletRepositoryMock, num_txs=1) -> tuple[list[tuple[User, TX]], dict]:
        txs = []
        targets = {}

        for vault in cache.get_all_user_vaults():
            targets[vault] = Decimal(str(vault.total_balance()))

        async def create_random_deposit():
            to_vault = repository.get_random_vault()
            signer = repository.get_user_by_user_id(to_vault.user_id)

            amount = quantize(Decimal(random.choice([ 10, 50, 100, 125, 150, 300 ])))
            
            tx = create_deposit_tx({ 'to_vault': to_vault, 'amount': amount })

            targets[to_vault] += amount

            txs.append((signer, tx))
        
        async def create_random_withdraw():
            from_vault = repository.get_random_vault()
            signer = repository.get_user_by_user_id(from_vault.user_id)

            amount = quantize(from_vault.balance * Decimal(random.choice([ 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25 ])))
            
            tx = create_withdrawal_tx({ 'from_vault': from_vault, 'amount': amount })

            if targets[from_vault] - amount >= 0:
                targets[from_vault] -= amount

            txs.append((signer, tx))
        
        for _ in range(0, num_txs):
            selected_template = random.choice([ 'DEPOSIT', 'WITHDRAW' ])

            if selected_template == 'DEPOSIT':
                await create_random_deposit()
            elif selected_template == 'WITHDRAW':
                await create_random_withdraw()

        return (txs, targets)
    
    async def tx_flow(self, tx_count: int, tx_proc: TXProcessor, signer: User, tx: TX) -> None:
        paygate = tx_proc.paygate

        loop = asyncio.get_event_loop()
        action_done = loop.create_future()

        async def random_paygate_webhook():
            await asyncio.sleep(random.choice([ 0.1, 0.15, 0.2, 0.25 ]))

            if len(paygate.pending_payments) == 0:
                return

            webhook_ref_header = paygate.pending_payments.pop()
            
            tx = tx_proc.get_tx_from_webhook(webhook_ref_header)

            assert tx is not None

            async def pop_callback(pop_result: TXPopResult):
                action_done.set_result(True)

                print(f'[{pop_result.timestamp}] TX {tx_count} pop')
            
            await tx_proc.pop_tx_with_callback(pop_callback, tx)

        async def push_callback(push_result: TXPushResult):
            print(f'[{push_result.timestamp}] TX {tx_count} push')

            if push_result.with_error():
                action_done.set_result(True)
                return

            await random_paygate_webhook()

        await tx_proc.push_tx_with_callback(push_callback, signer, tx)

        await action_done

    def verify_balance_targets(self, cache: WalletCacheMock, repository: WalletRepositoryMock, targets: dict):
        cache_vaults = cache.get_all_user_vaults()
        rep_vaults = repository.get_all_user_vaults()

        for vault in cache_vaults:
            assert targets[vault] == vault.total_balance()

        for vault in rep_vaults:
            assert targets[vault] == vault.total_balance()
    
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_random_tx_batch_sequence(self):
        (cache, repository, paygate) = get_back_context({
            'num_users': 10,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': True,
                'locked': False
            }
        })

        tx_proc = TXProcessor(cache, repository, paygate, 
            config=TXProcessorConfig(
                tx_queue_type=TX_QUEUE_TYPE.SERVER_SINGLE
            )
        )

        (txs, targets) = await self.get_random_tx_batch(cache, repository, num_txs=50)

        promises = []

        print('')

        async def process_simultaneous():
            tx_count = 1
            
            for (signer, tx) in txs:
                promises.append(self.tx_flow(tx_count, tx_proc, signer, tx))
                tx_count += 1

            print(f'Processing {len(txs)} transactions...')
            await asyncio.gather(*promises)
            print('Done')

        async def process_1by1():
            tx_count = 1

            for (signer, tx) in txs:
                await self.tx_flow(tx_count, tx_proc, signer, tx)
                tx_count += 1
        
        await process_1by1()

        self.verify_balance_targets(cache, repository, targets)

        assert True