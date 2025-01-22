import pytest

from src.routes.wallet.set_pix_key import Controller as SetPixKeyController
from src.routes.wallet.withdrawal import Controller as WithdrawalController

from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock

from src.shared.wallet.enums.pix import PIX_KEY_TYPE

from tests.shared.wallet.mocks.common import get_back_context

pytest_plugins = ('pytest_asyncio')

class Test_Deposit:
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_controller(self):
        set_pix_key_controller = SetPixKeyController()
        withdrawal_controller = WithdrawalController()

        (cache, repository, paygate) = await get_back_context({
            'num_users': 1,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': True,
                'locked': False
            },
            'singleton': True
        })

        user = repository.get_random_user()

        def post_set_pix_key():
            body = {
                "requester_user": user.to_api_dto(),
                "pix_key": { 
                    "type": PIX_KEY_TYPE.CPF.value,
                    "value": "85223578970" 
                }
            }

            request = HttpRequest(body=body, headers={}, query_params={})

            response = set_pix_key_controller.execute(request)

            assert response.status_code == 200
        
        async def post_withdrawal():
            body = {
                "requester_user": user.to_api_dto(),
                "amount": 200
            }

            request = HttpRequest(body=body, headers={}, query_params={})

            response = await withdrawal_controller.execute(request)

            assert response.status_code == 200

            body = response.body

            assert 'withdrawal_result' in body
            
            withdrawal_result = body['withdrawal_result']

            assert withdrawal_result['error'] == ''
            assert 'sign_result' in withdrawal_result

            sign_result = withdrawal_result['sign_result']

            assert 'data' in sign_result
            assert 'pix_url' in sign_result['data']

        post_set_pix_key()
        await post_withdrawal()
