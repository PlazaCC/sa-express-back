import pytest

from tests.routes.wallet.common import load_app_env, initialize_mocks

load_app_env()

from src.routes.transfer.transfer import Controller

from src.shared.helpers.external_interfaces.http_models import HttpRequest

pytest_plugins = ('pytest_asyncio')

class Test_Transfer:
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_controller(self):
        (cache, repository, paygate) = initialize_mocks()

        users = repository.get_all_users()

        src_user = users[0]
        dst_user = users[1]

        async def post_transfer():
            body = {
                'requester_user': src_user.to_api_dto(),
                'dst_user_email': dst_user.email,
                'amount': '200'
            }
            
            request = HttpRequest(body=body, headers={}, query_params={})

            response = await Controller().execute(request)

            assert response.status_code == 200

            body = response.body
            
            assert 'tx_id' in body
            assert 'result' in body
            
            transfer_result = body['result']

            assert transfer_result['error'] == ''
            assert 'sign_result' in transfer_result

            sign_result = transfer_result['sign_result']
            commit_result = transfer_result['commit_result']

            assert sign_result['error'] == ''
            assert commit_result['error'] == ''
            
            assert True

        await post_transfer()
