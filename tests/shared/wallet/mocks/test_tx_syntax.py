import pytest
import random
import asyncio
from random import randrange

from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.domain.entities.tx import TX

from src.shared.wallet.decimal import Decimal
from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.enums.paygate_tx_status import PAYGATE_TX_STATUS
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.tx_results.pop import TXPopResult
from src.shared.wallet.tx_results.push import TXPushResult
from src.shared.wallet.tx_templates.deposit import create_deposit_tx
from src.shared.wallet.tx_templates.withdrawal import create_withdrawal_tx

from tests.shared.wallet.mocks.common import get_back_context

pytest_plugins = ('pytest_asyncio')

class Test_TXSyntax:
    ### UTILITY METHODS ###
    async def sign_txs(self, tx_proc: TXProcessor, txs: list[TX], paygate_tx_status: list[PAYGATE_TX_STATUS]):
        webhooks = []

        async def random_paygate_webhook():
            await asyncio.sleep(randrange(1, 3))

            paygate_ref = tx_proc.paygate.pending_payments.pop()
            
            tx = tx_proc.get_tx_by_paygate_ref(paygate_ref)

            assert tx is not None

            ptx_status = random.choice(paygate_tx_status)

            if ptx_status == PAYGATE_TX_STATUS.CONFIRMED:
                commit_result = await tx_proc.commit_tx_confirmed(tx)

                assert commit_result.without_error()
            elif ptx_status == PAYGATE_TX_STATUS.FAILED:
                commit_result = await tx_proc.commit_tx_failed(tx, f'Transaction failed on paygate with status "{ptx_status.value}"')

                assert commit_result.with_error()
        
        for (signer, tx) in txs:
            sign_result = await tx_proc.sign(signer, tx)
    
            assert sign_result.without_error()

            webhooks.append(random_paygate_webhook())

        await asyncio.gather(*webhooks)

    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_vaults(self):
        (cache, repository, paygate) = get_back_context({
            'num_users': 10,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': True,
                'locked': False
            }
        })

        cached_vaults = cache.get_all_vaults()

        assert len(cached_vaults) > 0

        total_balance = 0

        for vault in cached_vaults:
            total_balance += vault.balance

        assert total_balance > 0
    
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_deposits(self):
        (cache, repository, paygate) = get_back_context({
            'num_users': 10,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': False,
                'locked': False
            }
        })
        
        tx_proc = TXProcessor(cache, repository, paygate)
        
        txs = []

        for _ in range(0, 1):
            to_vault = repository.get_random_vault()
            signer = repository.get_user_by_user_id(to_vault.user_id)

            amount = Decimal(150)
            
            tx = create_deposit_tx({ 'to_vault': to_vault, 'amount': amount })

            txs.append((signer, tx))

        assert(len(txs) > 0)

        await self.sign_txs(tx_proc, txs, [ PAYGATE_TX_STATUS.CONFIRMED ])

        assert True
    
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_withdrawals(self):
        (cache, repository, paygate) = get_back_context({
            'num_users': 10,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': True,
                'locked': False
            }
        })
        
        tx_proc = TXProcessor(cache, repository, paygate)

        txs = []

        for _ in range(0, 1):
            from_vault = repository.get_random_vault()
            signer = repository.get_user_by_user_id(from_vault.user_id)

            amount = from_vault.balance * Decimal(0.1)
            
            tx = create_withdrawal_tx({ 'from_vault': from_vault, 'amount': amount })

            txs.append((signer, tx))

        assert(len(txs) > 0)

        await self.sign_txs(tx_proc, txs, [ PAYGATE_TX_STATUS.CONFIRMED ])

        assert True
    
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_client_queue(self):
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
                tx_queue_type=TX_QUEUE_TYPE.CLIENT
            )
        )

        to_vault = repository.get_random_vault()
        signer = repository.get_user_by_user_id(to_vault.user_id)

        amount = Decimal(150)
        
        tx = create_deposit_tx({ 'to_vault': to_vault, 'amount': amount })

        async def random_paygate_webhook():
            await asyncio.sleep(randrange(1, 3))

            paygate_ref = tx_proc.paygate.pending_payments.pop()
            
            tx = tx_proc.get_tx_by_paygate_ref(paygate_ref)

            assert tx is not None

            async def callback(pop_result: TXPopResult):
                assert pop_result.without_error()

            await tx_proc.pop_tx_with_callback(callback, tx)

        push_result = await tx_proc.push_tx(signer, tx)
        
        assert push_result.without_error()

        await random_paygate_webhook()

        assert True
    
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_server_single_queue(self):
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

        to_vault = repository.get_random_vault()
        signer = repository.get_user_by_user_id(to_vault.user_id)

        amount = Decimal(150)
        
        tx = create_deposit_tx({ 'to_vault': to_vault, 'amount': amount })

        async def random_paygate_webhook():
            await asyncio.sleep(randrange(1, 3))

            paygate_ref = tx_proc.paygate.pending_payments.pop()
            
            tx = tx_proc.get_tx_by_paygate_ref(paygate_ref)

            assert tx is not None

            async def pop_callback(pop_result: TXPopResult):
                assert pop_result.without_error()

            await tx_proc.pop_tx_with_callback(pop_callback, tx)

        async def push_callback(push_result: TXPushResult):
            assert push_result.without_error()

            await random_paygate_webhook()

        await tx_proc.push_tx_with_callback(push_callback, signer, tx)

        await asyncio.sleep(1)

        assert True