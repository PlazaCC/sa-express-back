
from datetime import time
import uuid
from src.shared.domain.entities.deal import Deal
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.repository import Repository


class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')
            
            requester_user = request.data.get('requester_user')

            if requester_user.role != ROLE.ADMIN and requester_user.role != ROLE.OPERADOR:
                raise ForbiddenAction('Usuário não autorizado')

            if request.data.get('entity_id') is None:
                raise MissingParameters('entity_id')
            
            if request.data.get('deal_id') is None:
                raise MissingParameters('deal_id')

            response = Usecase().execute(
                entity_id=request.data.get('entity_id'),
                deal_id=request.data.get('deal_id'),
            )
            
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
        self.repository = Repository(deal_repo=True)
        self.deal_repo = self.repository.deal_repo

    def execute(self, entity_id: str, deal_id: str) -> dict:

        deal = self.deal_repo.delete_deal(
            entity_id=entity_id,
            deal_id=deal_id
        )

        return deal.to_dict()

def function_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()