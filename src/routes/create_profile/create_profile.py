from typing import List
from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.entities.profile import Profile
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import DuplicatedItem, EntityError, MissingParameters, WrongTypeParametersError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Created, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.repository import Repository
from datetime import datetime


class Controller:
  @staticmethod
  def execute(request: IRequest) -> IResponse:
    try:
      if request.data.get('requester_user') is None:
        raise MissingParameters('requester_user')
            
      requester_user = request.data.get('requester_user')
      
      user_id = requester_user.user_id
      role = requester_user.role
      entity_id = request.data.get("entity_id")
      
      if not user_id:
        raise MissingParameters("user_id")
      if not role:
        raise MissingParameters("role")
      
      if role not in ROLE._member_names_:
        raise EntityError('Cargo inválido')
      
      role = ROLE[role]

      if (role == ROLE.OPERADOR) and (entity_id is None):
        raise MissingParameters("entity_id")
      
      response = Usecase().execute(
        user_id=user_id,
        role=role,
        entity_id=entity_id
      )
      
      return Created(body=response)
    
    except MissingParameters as error:
      return BadRequest(error.message)
    except WrongTypeParametersError as error:
      return BadRequest(error.message)
    except EntityError as error:
      return BadRequest(error.message)
    except ValueError as error:
      return BadRequest(error.args[0])
    except Exception as error:
      return InternalServerError(str(error))
    
class Usecase:
  repository: Repository
  
  def __init__(self):
    self.repository = Repository(profile_repo=True)
    self.profile_repo = self.repository.profile_repo
    
  def execute(self, user_id: str, role: ROLE, entity_id: str = None) -> dict:
    profile_exists = self.profile_repo.get_profile_by_user_id(user_id)
    
    if profile_exists:
      raise DuplicatedItem("perfil")
    
    profile = Profile(
      user_id=user_id,
      role=role,
      entity_id=entity_id,
      status=True,
      created_at=int(datetime.now().timestamp()),
      updated_at=int(datetime.now().timestamp())
    )
    
    profile = self.profile_repo.create_profile(profile=profile)

    return {
      "profile": profile.to_dict(), 
      "message": "Perfil criado com sucesso"
    }
  
def function_handler(event, context):
  http_request = LambdaHttpRequest(data=event)
  http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
  response = Controller.execute(http_request)
  http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  
  return http_response.toDict()