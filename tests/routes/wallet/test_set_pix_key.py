import pytest

from tests.routes.wallet.common import load_app_env, initialize_mocks

load_app_env()

from src.routes.set_pix_key.set_pix_key import Controller

from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock

from src.shared.wallet.enums.pix import PIX_KEY_TYPE

class Test_SetPIXKey:
    ### TEST METHODS ###
    # @pytest.mark.skip(reason='')
    def test_controller(self):
        (cache, repository, paygate) = initialize_mocks()

        user = repository.get_random_user()

        body = {
            'requester_user': user.to_api_dto(),
            'pix_key': { 
                'type': PIX_KEY_TYPE.CPF.value,
                'value': '85223578970' 
            }
        }
        
        request = HttpRequest(body=body, headers={}, query_params={})

        response = Controller().execute(request)

        assert response.status_code == 200