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

class Test_TXStressMock:
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_tx_efficacy(self):
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

        assert True