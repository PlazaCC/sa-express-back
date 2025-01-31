from http.client import CREATED, OK
from src.shared.domain.entities.entity import Banner, Entity
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters, NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.repository import Repository


class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(entity_repo=True)
        self.entity_repo = self.repository.entity_repo
    
    def execute(self, deal_id: str, status: str) -> dict:
        deal = self.entity_repo.get_entity_deal(deal_id)

        if deal is None:
            raise NoItemsFound('Deal not found')
        
        if deal.deal_status == status:
            raise EntityError('Status do deal nao pode ser o mesmo')
        
        deal_updated = self.entity_repo.update_deal_status(deal=deal, new_status=status)

        return deal_updated.to_dict()
        

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:         
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')
            
            requester_user = request.data.get('requester_user')

            if requester_user.role != ROLE.ADMIN and requester_user.role != ROLE.OPERADOR:
                raise ForbiddenAction('Usuário não autorizado')
            
            if request.data.get('deal_id') is None:
                raise MissingParameters('deal_id')
            
            if request.data.get('status') is None:
                raise MissingParameters('status')
            
            if request.data.get('status') not in DEAL_STATUS._member_names_:
                raise EntityError('Status inválido')
            
            response = Usecase().execute(
                deal_id=request.data.get('deal_id'),
                status=request.data.get('status'),
            )
        
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return Forbidden(error.message)
        except EntityError as error:
            return BadRequest(error.message)
        except ValueError as error:
            return BadRequest(error.args[0])
        except Exception as error:
            return InternalServerError(str(error))

def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()