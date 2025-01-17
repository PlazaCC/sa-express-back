import pytest
import random
import asyncio
from decimal import Decimal
from random import randrange

from src.shared.domain.enums.user_status_enum import USER_STATUS

from src.shared.domain.entities.tx import TX

from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.enums.paygate_tx_status import PAYGATE_TX_STATUS
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.tx_results.pop import TXPopResult
from src.shared.wallet.tx_results.push import TXPushResult
from src.shared.wallet.tx_templates.deposit import create_deposit_tx
from src.shared.wallet.tx_templates.withdrawal import create_withdrawal_tx

from tests.shared.wallet.mocks.common import get_back_context

pytest_plugins = ('pytest_asyncio')

class Test_TXEfficacy:
    ### UTILITY METHODS ###
    async def get_random_tx_batch(self, cache, repository, num_txs=1):
        initial_balance_inrep = Decimal(0)
        initial_balance_incache = Decimal(0)
        
        rep_vaults = repository.get_all_user_vaults()

        for vault in rep_vaults:
            initial_balance_inrep += vault.total_balance()
        
        cache_vaults = cache.get_all_user_vaults()

        for vault in cache_vaults:
            initial_balance_incache += vault.total_balance()

        txs = []
        desired_vault_balances = {}

        for vault in cache_vaults:
            desired_vault_balances[vault] = vault.total_balance()

        async def create_random_deposit():
            to_vault = repository.get_random_vault()
            (_, signer) = await repository.get_user_by_user_id(to_vault.user_id)

            amount = Decimal(random.choice([ 10, 50, 100, 125, 150, 300 ]))
            
            tx = create_deposit_tx({ 'to_vault': to_vault, 'amount': amount })

            desired_vault_balances[to_vault] += amount

            txs.append((signer, tx))
        
        async def create_random_withdraw():
            from_vault = repository.get_random_vault()
            (_, signer) = await repository.get_user_by_user_id(from_vault.user_id)

            amount = from_vault.balance * Decimal(random.choice([ 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25 ]))
            
            tx = create_withdrawal_tx({ 'from_vault': from_vault, 'amount': amount })

            desired_vault_balances[from_vault] = max(0, desired_vault_balances[from_vault] - amount)

            txs.append((signer, tx))
        
        for _ in range(0, num_txs):
            selected_template = random.choice([ 'DEPOSIT', 'WITHDRAW' ])

            if selected_template == 'DEPOSIT':
                await create_random_deposit()
            elif selected_template == 'WITHDRAW':
                await create_random_withdraw()

        return {
            'initial_balance_incache': initial_balance_incache,
            'initial_balance_inrep': initial_balance_inrep,
            'desired_vault_balances': desired_vault_balances,
            'txs': txs,
        }
    
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_random_tx_batch_sequence(self):
        (cache, repository, paygate) = await get_back_context({
            'num_users': 10,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': True,
                'locked': False
            }
        })

        tx_proc = TXProcessor(cache, repository, paygate, 
            config=TXProcessorConfig(
                max_vaults=2,
                max_instructions=1,
                tx_queue_type=TX_QUEUE_TYPE.CLIENT
            )
        )

        tx_batch = await self.get_random_tx_batch(cache, repository, num_txs=10)

        

        print('tx_batch', tx_batch)

        assert True