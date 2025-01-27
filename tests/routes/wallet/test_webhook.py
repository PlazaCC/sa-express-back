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
            'X-Webhook-Signature': 'HMAC-SHA256 Sign=5D90499D59FB0D9FAD44A15112936CFCABA73A6EE666AAA63B60A0FC03F40EA5,Nonce=b7891a74-ca9a-4770-bedd-8fd8341b122b,TS=1684633816',
            'X-Webhook-Reference': Paybrokers.get_paygate_ref_header(deposit_tx.tx_id, deposit_tx.nonce)
        }

        body = {
            'id': 'f6431a0f-970a-4be9-9c6d-f444f729adc3',
            'transactionState': 'Completed',
            'transactionDate': '2023-05-19T19:51:21.320Z',
            'transactionAmount': '0.010000',
            'transactionType': 'Credit',
            'transactionPaymentType': 'PIX',
            'payer': { 
                'name': 'Johnny Boy',
                'taxNumber': '09977799400'
            }
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
            'X-Webhook-Signature': 'HMAC-SHA256 Sign=5D90499D59FB0D9FAD44A15112936CFCABA73A6EE666AAA63B60A0FC03F40EA5,Nonce=b7891a74-ca9a-4770-bedd-8fd8341b122b,TS=1684633816',
            'X-Webhook-Reference': Paybrokers.get_paygate_ref_header(withdrawal_tx.tx_id, withdrawal_tx.nonce)
        }

        body = {
            'id': 'f6431a0f-970a-4be9-9c6d-f444f729adc3',
            'transactionState': 'Completed',
            'transactionDate': '2023-05-19T19:51:21.320Z',
            'transactionAmount': '0.010000',
            'transactionType': 'Credit',
            'transactionPaymentType': 'PIX',
            'payer': { 
                'name': 'Johnny Boy',
                'taxNumber': '09977799400'
            }
        }

        request = HttpRequest(body=body, headers=headers, query_params={})

        response = await PaybrokersWebhookController().execute(request)

        assert response.status_code == 200
