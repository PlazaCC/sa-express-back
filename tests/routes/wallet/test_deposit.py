import pytest

from tests.routes.wallet.common import load_app_env, initialize_mocks

load_app_env()

from src.routes.deposit.deposit import Controller

from src.shared.helpers.external_interfaces.http_models import HttpRequest

pytest_plugins = ('pytest_asyncio')

class Test_Deposit:
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_controller(self):
        (cache, repository, paygate) = initialize_mocks()

        user = repository.get_random_user()

        async def post_deposit():
            body = {
                'requester_user': user.to_api_dto(),
                'amount': '200'
            }
            
            request = HttpRequest(body=body, headers={}, query_params={})

            response = await Controller().execute(request)

            assert response.status_code == 200

            body = response.body

            assert 'tx_id' in body
            assert 'result' in body
            
            deposit_result = body['result']

            assert deposit_result['error'] == ''
            assert 'sign_result' in deposit_result

            sign_result = deposit_result['sign_result']

            assert 'data' in sign_result
            assert 'pix_qrcode' in sign_result['data']

        await post_deposit()
