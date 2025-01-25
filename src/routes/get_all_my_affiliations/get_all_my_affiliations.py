from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError
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
          response = Usecase().execute(requester_user)
          return OK(body=response)
            
        except MissingParameters as error:
          return BadRequest(error.message)
        except ForbiddenAction as error:
          return Forbidden(error.message)
        except EntityError as error:
          return BadRequest(error.args[0])
        except ValueError as error:
          return BadRequest(error.args[0])
        except Exception as error:
          return InternalServerError(str(error))
            
            

class Usecase:
  repository: Repository
  
  def __init__(self):
        self.repository = Repository(affiliation_repo=True)
        self.affiliation_repo = self.repository.affiliation_repo
        
  def execute(self, requester_user: AuthAuthorizerDTO):
    user_id = requester_user.user_id
    
    affiliations = self.affiliation_repo.get_all_my_affiliations(user_id)
    
    return {
      "affiliations": [affiliation.to_dict() for affiliation in affiliations],
      "message": "Afiliações encontradas com sucesso"
    }
  
def function_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()
    
    
  