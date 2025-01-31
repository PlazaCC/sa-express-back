import uuid
from datetime import time
from src.shared.domain.entities.entity import Banner, Entity
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.repository import Repository

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(entity_repo=True)
        self.entity_repo = self.repository.entity_repo
    
    def execute(self, entity_id: str) -> dict:
        entity = self.entity_repo.get_entity(entity_id)

        return entity.to_dict()

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:         
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')
            
            requester_user = request.data.get('requester_user')

            if requester_user.role != ROLE.ADMIN:
                raise ForbiddenAction('Usuário não autorizado')
            
            if request.data.get('entity_id') is None:
                raise MissingParameters('entity_id')
            
            response = Usecase().execute(
                entity_id=request.data.get('entity_id')
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