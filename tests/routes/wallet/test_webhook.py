import pytest

from src.routes.wallet.paybrokers_webhook import Controller as PaybrokersWebhookController

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.shared.wallet.wrappers.paybrokers import Paybrokers

from tests.routes.wallet.common import initialize_mocks, deposit_mock, withdrawal_mock

pytest_plugins = ('pytest_asyncio')

class Test_Deposit:
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_paygate_deposit(self):
        (cache, repository, paygate) = initialize_mocks()

        (deposit_tx, push_result) = await deposit_mock(cache, repository, paygate)

        headers = {
            'PAYGATE_AUTH': Paybrokers.get_paygate_auth_header(deposit_tx.tx_id, deposit_tx.nonce)
        }

        body = {
            'id': '9947b80a-8107-4264-938d-56a7f43593f5',
            'transactionState': 'Completed',
            'transactionDate': '2023-05-19T19:51:21.320Z',
            'transactionAmount': '150',
            'transactionType': 'Credit',
            'transactionPaymentType': 'PIX',
        }
        
        request = HttpRequest(body=body, headers=headers, query_params={})

        response = await PaybrokersWebhookController().execute(request)

        assert response.status_code == 200

    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_paygate_withdrawal(self):
        (cache, repository, paygate) = initialize_mocks()

        (withdrawal_tx, push_result) = await withdrawal_mock(cache, repository, paygate)

        headers = {
            'PAYGATE_AUTH': Paybrokers.get_paygate_auth_header(withdrawal_tx.tx_id, withdrawal_tx.nonce)
        }

        request = HttpRequest(body={}, headers=headers, query_params={})

        response = await PaybrokersWebhookController().execute(request)

        assert response.status_code == 200
