from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import ForbiddenAction, MissingParameters, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound, Unauthorized
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.infra.repositories.repository import Repository


class Controller:
  @staticmethod
  def execute(request: IRequest) -> IResponse:
    try:
      if request.data.get('requester_user') is None:
          raise MissingParameters('requester_user')
            
      requester_user = AuthAuthorizerDTO(**request.data.get('requester_user'))
        
      response = Usecase().execute( requester_user )
      
      return OK(body=response)
    except MissingParameters as error:  
      return BadRequest(error.message)
    except NoItemsFound as error:
      return NotFound(error.message)
    except ForbiddenAction as error:
      return Unauthorized(error.message)
    except Exception as error:
      return InternalServerError(error.args[0])
    
class Usecase:
  repository: Repository
  
  def __init__(self):
    self.repository = Repository(profile_repo=True)
    self.profile_repo = self.repository.profile_repo
  
  def execute(self, requester_user: AuthAuthorizerDTO):
    profile_exists = self.profile_repo.get_profile_by_id(requester_user.user_id)
    
    if not profile_exists:
      raise NoItemsFound("perfil não encontrado")
    
    profile = self.profile_repo.deactivate_profile(requester_user.user_id)
    
    dict_response = {
      "profile": profile.to_dict(),
      "message": "Perfil desativado com sucesso"
    }
    
    return dict_response
  
  
def function_handler(event, context):
  http_request = LambdaHttpRequest(data=event)
  http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
  response = Controller.execute(http_request)
  http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  
  return http_response.toDict()