
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
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
            
            if request.data.get('entity_id') is None:
                raise MissingParameters('entity_id')
            
            if request.data.get('last_evaluated_key') is None:
                last_evaluated_key = None
            else:
                last_evaluated_key = request.data.get('last_evaluated_key')
                        
            response = Usecase().execute(entity_id=request.data.get('entity_id'), last_evaluated_key=last_evaluated_key)
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return Forbidden(error.message)
        except EntityError as error:
            return BadRequest(error.message)
        except ValueError as error:
            return BadRequest(error.message)
        except Exception as error:
            return InternalServerError(str(error))

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(entity_repo=True)
        self.entity_repo = self.repository.entity_repo

    def execute(self, entity_id: str, last_evaluated_key: str) -> dict:
        deals = self.entity_repo.get_entity_deals(
            entity_id=entity_id,
            status=DEAL_STATUS.ACTIVATED.value,
            last_evaluated_key=last_evaluated_key
        )
        return [deal.to_dict() for deal in deals]

def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()