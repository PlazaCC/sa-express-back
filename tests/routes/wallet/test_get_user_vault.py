import pytest

from src.routes.get_user_vault.get_user_vault import Controller

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from tests.routes.wallet.common import initialize_mocks

class Test_GetUserVault:
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