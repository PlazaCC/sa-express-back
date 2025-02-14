from src.shared.helpers.errors.errors import ForbiddenAction
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, Unauthorized
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.infra.repositories.repository import Repository


class Controller:
  @staticmethod
  def execute(request: IRequest) -> IResponse:
    try:
      
      requester_user = AuthAuthorizerDTO(**request.data.get('requester_user'))
      
      if not requester_user:
        raise ForbiddenAction('requester_user não encontrado')
      
      last_evaluated_key = request.data.get('last_evaluated_key')
      limit = request.data.get('limit')
      
      if limit and type(limit) != str:
        raise ValueError('limit deve ser uma string')
      
      if last_evaluated_key and type(last_evaluated_key) != str:
        raise ValueError('last_evaluated_key deve ser uma string')
      
      response = Usecase().execute(
        last_evaluated_key=last_evaluated_key,
        limit=int(limit) if limit else None,
      )
      
      return OK(body=response)
    
    except ForbiddenAction as error:
      return Unauthorized(error.message)
    except ValueError as error:
      return BadRequest(error.args[0])
    except Exception as error:
      return InternalServerError(str(error))
      
      
      
class Usecase:
  repository: Repository
  
  def __init__(self):
    self.repository = Repository(influencer_repo=True)
    self.influencer_repo = self.repository.influencer_repo
    
  
  def execute(self, last_evaluated_key: str, limit: int) -> dict:
    data = self.influencer_repo.get_all_influencers(last_evaluated_key, limit)
    
    influencers = data.get('influencers', [])
    last_evaluated_key = data.get('last_evaluated_key')
    
    response_dict = {
      'influencers': [influencer.to_dict() for influencer in influencers],
      'last_evaluated_key': last_evaluated_key
    }
    
    return response_dict
    