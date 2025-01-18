from src.routes.wallet.create_vault import Controller, Usecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock

class Test_CreateVault:
    def test_usecase(self):
        usecase = Usecase()
        
        response = usecase.execute()

        assert len(response) == 2

    def test_controller(self):
        controller = Controller()

        request = HttpRequest(body={}, headers={}, query_params={})

        response = controller.execute(request)

        assert response.status_code == 200
        assert len(response.body) == 2