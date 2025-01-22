from typing import List
from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.entities.profile import Profile
from src.shared.domain.enums.profile_status_enum import PROFILE_STATUS
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
      bet_data_id = request.data.get("bet_data_id")
      game_data_id = request.data.get("game_data_id")
      affiliations = request.data.get("affiliations")
      wallet_id = request.data.get("wallet_id")
      status = request.data.get("status")
      
      if not user_id:
        raise MissingParameters("user_id")
      if not role:
        raise MissingParameters("role")
      if not bet_data_id:
        raise MissingParameters("bet_data_id")
      if not game_data_id:
        raise MissingParameters("game_data_id")
      if not affiliations:
        raise MissingParameters("affiliations")
      if not wallet_id:
        raise MissingParameters("wallet_id")
      
      if status and not isinstance(status, str):
        raise WrongTypeParametersError("status", "str", type(status))
      
      """
      AFILIADO = 'AFILIADO'
      SUBAFILIADO = 'SUBAFILIADO'
      INFLUENCER = 'INFLUENCER'
      EMBAIXADOR = 'EMBAIXADOR'
      OPERADOR = 'OPERADOR'
      ADMIN = 'ADMIN'
      """
      
      if role not in ["AFILIADO", "SUBAFILIADO", "INFLUENCER", "EMBAIXADOR", "OPERADOR", "ADMIN"]:
        raise ValueError('Cargo inválido')
      
      
      
      if type(user_id) != str:
        raise WrongTypeParametersError("user_id", "str", type(user_id))
      
      if type(bet_data_id) != str:
        raise WrongTypeParametersError("bet_data_id", "str", type(bet_data_id))
      
      if type(game_data_id) != str:
        raise WrongTypeParametersError("game_data_id", "str", type(game_data_id))
      
      if affiliations and not isinstance(affiliations, list):
        raise WrongTypeParametersError("affiliations", "list", type(affiliations))
      
      for affiliation in affiliations:
        if not isinstance(affiliation, Affiliation):
          raise WrongTypeParametersError("affiliation", "Affiliation", type(affiliation))
      
      if type(wallet_id) != str:
        raise WrongTypeParametersError("wallet_id", "str", type(wallet_id))
      
      if status and status not in ["ACTIVE", "INACTIVE"]:
        raise ValueError("Status deve ser 'ACTIVE' ou 'INACTIVE'")
      
      response = Usecase().execute(user_id, bet_data_id, game_data_id, affiliations, wallet_id, status, role)
      
      return Created(body=response)
    
    except MissingParameters as error:
      return BadRequest(error.message)
    except WrongTypeParametersError as error:
      return BadRequest(error.message)
    except EntityError as error:
      return BadRequest(error.args[0])
    except ValueError as error:
      return BadRequest(error.args[0])
    except Exception as error:
      return InternalServerError(str(error))
    
class Usecase:
  repository: Repository
  
  def __init__(self):
    self.repository = Repository(profile_repo=True)
    self.profile_repo = self.repository.profile_repo
    
  def execute(self, user_id: str, bet_data_id: str, game_data_id: str, affiliations: List[Affiliation], wallet_id: str, status: str, role: str) -> dict:
    profile_exists = self.profile_repo.get_profile_by_user_id(user_id)
    if profile_exists:
      raise DuplicatedItem("perfil já existente")
    profile = Profile(user_id, bet_data_id, game_data_id, affiliations, wallet_id, PROFILE_STATUS[status], ROLE[role], datetime.now().timestamp(), datetime.now().timestamp())
    self.profile_repo.create_profile(profile)
    return {"profile": profile.to_dict(), "message": "Perfil criado com sucesso"}
  
def function_handler(event, context):
  http_request = LambdaHttpRequest(data=event)
  http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
  response = Controller.execute(http_request)
  http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  
  return http_response.toDict()