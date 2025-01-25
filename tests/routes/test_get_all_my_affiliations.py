from src.routes.get_all_my_affiliations.get_all_my_affiliations import Usecase, Controller
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO


class Test_GetAllMyAffiliations:
    def test_usecase(self):
        usecase = Usecase()
        requester_user = AuthAuthorizerDTO(
            user_id="00000000-0000-0000-0000-000000000000",
            name="Rodrigo Siqueira",
            role="ADMIN",
            email="email@email.com",
            email_verified=True,
        )
        
        response = usecase.execute(requester_user)
        
        assert response.get("message") == "Afiliações encontradas com sucesso"
        assert len(response.get("affiliations")) == 1
        
    def test_usecase_with_no_affiliations(self):
        usecase = Usecase()
        requester_user = AuthAuthorizerDTO(
            user_id="10000000-0000-0000-0000-000000000000",
            name="Rodrigo Siqueira",
            role="ADMIN",
            email="email@email.com",
            email_verified=True,
        )
        
        response = usecase.execute(requester_user)
        
        assert len(response.get("affiliations")) == 0
        
    def test_controller(self):
        controller = Controller()
        request = HttpRequest(body= {
          "requester_user": {
            "user_id": "00000000-0000-0000-0000-000000000000",
            "name": "Rodrigo Siqueira",
            "role": "ADMIN",
            "email": "email@email.com",
            "email_verified": True,
          }
        }, headers={}, query_params={})
        
        response = controller.execute(request)
        
        assert response.data.get("message") == "Afiliações encontradas com sucesso"
        assert len(response.data.get("affiliations")) == 1
        
    def test_controller_missing_requester_user(self):
        controller = Controller()
        request = HttpRequest(body={}, headers={}, query_params={})
        
        response = controller.execute(request)
        
        assert response.status_code == 400
        assert response.data.get("body") == "Parâmetro ausente: requester_user"
        
    def test_controller_with_non_existent_user(self):
        controller = Controller()
        request = HttpRequest(body= {
          "requester_user": {
            "user_id": "10000000-0000-0000-0000-000000000000",
            "name": "Rodrigo Siqueira",
            "role": "ADMIN",
            "email": "email@email.com"
          }
        }, headers={}, query_params={})
        
        response = controller.execute(request)
        
        assert response.status_code == 200
        assert response.data.get("message") == "Afiliações encontradas com sucesso"
        assert len(response.data.get("affiliations")) == 0
        
      