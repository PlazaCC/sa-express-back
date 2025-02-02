import pytest
from src.routes.deactivate_profile.deactivate_profile import Usecase, Controller
from src.shared.helpers.errors.errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO


class Test_DeactivateProfile:
    def test_usecase(self):
        usecase = Usecase()
        requester_user = AuthAuthorizerDTO(
            user_id="00000000-0000-0000-0000-000000000000",
            name="Rodrigo Siqueira",
            role="ADMIN",
            email="email@email.com",
        )
        
        response = usecase.execute(requester_user)
        
        assert response.get("message") == "Perfil desativado com sucesso"
        assert response.get("profile").get("status") == False
        
    def test_usecase_with_non_existent_profile(self):
        usecase = Usecase()
        requester_user = AuthAuthorizerDTO(
            user_id="10000000-0000-0000-0000-000000000000",
            name="Rodrigo Siqueira",
            role="ADMIN",
            email="email@email.com"
        )
        
        with pytest.raises(NoItemsFound):
            usecase.execute(requester_user)
            
    def test_controller(self):
        controller = Controller()
        
        request = HttpRequest(body= {
          "requester_user": {
            "user_id": "00000000-0000-0000-0000-000000000000",
            "name": "Rodrigo Siqueira",
            "role": "ADMIN",
            "email": "email@email.com",
          }
        }, headers={}, query_params={})
        
        response = controller.execute(request)
        
        assert response.status_code == 200
        assert response.body.get("message") == "Perfil desativado com sucesso"
        
    def test_controller_missing_requester_user(self):
        controller = Controller()
        request = HttpRequest(body={}, headers={}, query_params={})
        
        response = controller.execute(request)
        
        assert response.status_code == 400
        assert response.data.get("body") == "Parâmetro ausente: requester_user"
        
    def test_controller_with_non_existent_profile(self):
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
        
        assert response.status_code == 404
        assert response.data.get("body") == "Nenhum item encontrado: perfil não encontrado"
        
    
        
        