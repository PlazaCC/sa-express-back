from src.routes.get_all_deals.get_all_deals import Controller, Usecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.mocks.deal_repository_mock import DealRepositoryMock


class Test_GetAllDeals:

    def test_usecase(self):
        usecase = Usecase()
        
        response = usecase.execute()

        assert len(response) == 2

    def test_controller(self):
        controller = Controller()

        request = HttpRequest(body={
            "requester_user": {
                'custom:general_role': 'ADMIN_COLLABORATOR',
            }
        }, headers={}, query_params={})

        response = controller.execute(request)

        assert response.status_code == 200
        assert len(response.body) == 2
    
    def test_controller_missing_requester_user(self):
        controller = Controller()

        request = HttpRequest(body={}, headers={}, query_params={})

        response = controller.execute(request)

        assert response.status_code == 400
        assert response.body== 'Parâmetro ausente: requester_user'