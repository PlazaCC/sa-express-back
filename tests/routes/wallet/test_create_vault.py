from src.routes.wallet.create_vault import Controller, Usecase

from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock

from tests.shared.wallet.mocks.repository import RepositoryMock

class Test_CreateVault:
    def test_controller(self):
        controller = Controller()
        repository = RepositoryMock()

        repository.generate_users({
            'num_users': 1,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
        })

        user = repository.get_random_user()

        body = {
            "requester_user": user.to_api_dto()
        }
        
        request = HttpRequest(body=body, headers={}, query_params={})

        response = controller.execute(request)

        assert response.status_code == 200