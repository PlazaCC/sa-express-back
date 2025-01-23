import pytest

from src.routes.wallet.paybrokers_webhook import Controller as PaybrokersWebhookController

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from tests.routes.wallet.common import initialize_mocks, deposit_mock, withdrawal_mock

pytest_plugins = ('pytest_asyncio')

class Test_Deposit:
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_paygate_deposit(self):
        (cache, repository, paygate) = initialize_mocks()

        (deposit_tx, push_result) = await deposit_mock(cache, repository, paygate)

        paygate_ref = push_result.sign_result.data['paygate_ref']

        query_params = {
            'paygate_ref': paygate_ref
        }
        
        request = HttpRequest(body={}, headers={}, query_params=query_params)

        response = await PaybrokersWebhookController().execute(request)

        assert response.status_code == 200

    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_paygate_withdrawal(self):
        (cache, repository, paygate) = initialize_mocks()

        (withdrawal_tx, push_result) = await withdrawal_mock(cache, repository, paygate)

        paygate_ref = push_result.sign_result.data['paygate_ref']

        query_params = {
            'paygate_ref': paygate_ref
        }
        
        request = HttpRequest(body={}, headers={}, query_params=query_params)

        response = await PaybrokersWebhookController().execute(request)

        assert response.status_code == 200
