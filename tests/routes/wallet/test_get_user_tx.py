import pytest

from src.routes.get_user_tx.get_user_tx import Controller

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from tests.routes.wallet.common import initialize_mocks, deposit_mock

pytest_plugins = ('pytest_asyncio')

class Test_GetUserTX:
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_basic(self):
        (cache, repository, paygate) = initialize_mocks()

        (deposit_tx, push_result) = await deposit_mock(cache, repository, paygate)

        user = repository.get_user_by_user_id(deposit_tx.user_id)

        body = {
            'requester_user': user.to_api_dto(),
            'tx_id': deposit_tx.tx_id
        }
        
        request = HttpRequest(body=body, headers={}, query_params={})

        response = Controller().execute(request)

        assert response.status_code == 200

        assert 'tx' in response.body
