import pytest

from src.routes.wallet.create_vault import Controller

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.shared.wallet.enums.pix import PIX_KEY_TYPE

from tests.routes.wallet.common import initialize_mocks

class Test_CreateVault:
    ### TEST METHODS ###
    # @pytest.mark.skip(reason='')
    def test_controller(self):
        (cache, repository, paygate) = initialize_mocks()

        user = repository.get_random_user()

        body = {
            'requester_user': user.to_api_dto()
        }
        
        request = HttpRequest(body=body, headers={}, query_params={})

        response = Controller().execute(request)

        assert response.status_code == 200

    # @pytest.mark.skip(reason='')
    def test_controller_with_pix(self):
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