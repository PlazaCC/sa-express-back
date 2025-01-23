import pytest

from src.routes.wallet.withdrawal import Controller

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from tests.routes.wallet.common import initialize_mocks

pytest_plugins = ('pytest_asyncio')

class Test_Deposit:
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_controller(self):
        (cache, repository, paygate) = initialize_mocks()

        user = repository.get_random_user()

        async def post_withdrawal():
            body = {
                'requester_user': user.to_api_dto(),
                'amount': '200'
            }

            request = HttpRequest(body=body, headers={}, query_params={})

            response = await Controller().execute(request)

            assert response.status_code == 200

            body = response.body

            assert 'withdrawal_result' in body
            
            withdrawal_result = body['withdrawal_result']

            assert withdrawal_result['error'] == ''
            assert 'sign_result' in withdrawal_result

            sign_result = withdrawal_result['sign_result']

            assert 'data' in sign_result
            assert 'paygate_ref' in sign_result['data']
            assert 'pix_key' in sign_result['data']

        await post_withdrawal()
