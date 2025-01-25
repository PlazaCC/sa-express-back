from src.routes.get_my_profile.get_my_profile import Controller, Usecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.infra.repositories.mocks.deal_repository_mock import DealRepositoryMock


class Test_Get_my_profile:


    def test_usecase(self):
        usecase = Usecase()
        requester_user = AuthAuthorizerDTO(
            user_id="00000000-0000-0000-0000-000000000000",
            name="Luca Gomes",
            role="ADMIN_COLLABORATOR",
            email="luca@email.com"
        )
        
        response = usecase.execute(requester_user)

        assert response["user_id"] == "00000000-0000-0000-0000-000000000000"
        assert response["entity_id"] == "00000000-0000-0000-0000-000000000000"
        assert response["game_data_id"] == "00000000-0000-0000-0000-000000000000"
        assert "affiliations" in response
        assert "wallet_id" in response




    def test_controller(self):
        controller = Controller()

        request = HttpRequest(body={
            "requester_user": {
                'user_id': '00000000-0000-0000-0000-000000000000',
                'name': 'Luca Gomes',
                'role': 'ADMIN_COLLABORATOR',
                'email': 'luca@email.com',
            }
        }, headers={}, query_params={})

        response = controller.execute(request)
        
        print(response.data)

        assert response.status_code == 200

        assert response.body["user_id"] == "00000000-0000-0000-0000-000000000000"
        assert response.body["entity_id"] == "00000000-0000-0000-0000-000000000000"
        assert response.body["game_data_id"] == "00000000-0000-0000-0000-000000000000"
        assert "affiliations" in response.body
        assert "wallet_id" in response.body


    
    def test_controller_missing_requester_user(self):
        controller = Controller()

        request = HttpRequest(body={}, headers={}, query_params={})

        response = controller.execute(request)

        assert response.status_code == 400
        assert response.body== 'Parâmetro ausente: requester_user'