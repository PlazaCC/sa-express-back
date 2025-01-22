import pytest

from src.routes.wallet.create_vault import Controller as CreateVaultController
from src.routes.wallet.deposit import Controller as DepositController

from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock

from src.shared.wallet.enums.pix import PIX_KEY_TYPE

pytest_plugins = ('pytest_asyncio')

class Test_Deposit:
    ### TEST METHODS ###
    @pytest.mark.asyncio
    # @pytest.mark.skip(reason='')
    async def test_controller(self):
        create_vault_controller = CreateVaultController()
        deposit_controller = DepositController()

        repository = WalletRepositoryMock()

        repository.generate_users({
            'append': True,
            'num_users': 1,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
        })

        user = repository.get_random_user()

        def post_create_vault():
            body = {
                "requester_user": user.to_api_dto(),
                "pix_key": { 
                    "type": PIX_KEY_TYPE.CPF.value,
                    "value": "85223578970" 
                }
            }

            request = HttpRequest(body=body, headers={}, query_params={})

            response = create_vault_controller.execute(request)

            assert response.status_code == 200

        # async def post_deposit():
        #     body = {
        #         "requester_user": user.to_api_dto(),
        #         "amount": 200
        #     }

        #     request = HttpRequest(body=body, headers={}, query_params={})

        #     response = await deposit_controller.execute(request)

        #     assert response.status_code == 200

        #     body = response.body

        #     assert 'deposit_result' in body
            
        #     deposit_result = body['deposit_result']

        #     assert deposit_result['error'] == ''
        #     assert 'sign_result' in deposit_result

        #     sign_result = deposit_result['sign_result']

        #     assert 'data' in sign_result
        #     assert 'pix_url' in sign_result['data']

        post_create_vault()
        # await post_deposit()
