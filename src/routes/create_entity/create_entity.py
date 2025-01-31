from http.client import CREATED
import uuid
from datetime import time
from src.shared.domain.entities.entity import Banner, Entity
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.http_codes import BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.repository import Repository


class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(entity_repo=True)
        self.entity_repo = self.repository.entity_repo
    
    def execute(self, name: str, logo_url: str, color: str, description: str) -> dict:
        entity = Entity(
            entity_id=uuid.uuid4(),
            name=name,
            description=description,
            banner=Banner(
                logo_url=logo_url,
                color=color
            ),
            created_at=int(round(time.time() * 1000)),
            updated_at=int(round(time.time() * 1000)),
        )

        entity_created = self.entity_repo.create_entity(entity)

        return entity_created.to_dict()

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:         
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')
            
            requester_user = request.data.get('requester_user')

            if requester_user.role != ROLE.ADMIN:
                raise ForbiddenAction('Usuário não autorizado')
            
            if request.data.get('name') is None:
                raise MissingParameters('name')
            
            if request.data.get('logo_url') is None:
                raise MissingParameters('logo_url')
            
            if request.data.get('color') is None:
                raise MissingParameters('color')
            
            if request.data.get('description') is None:
                raise MissingParameters('description')
            
            response = Usecase().execute(
                name=request.data.get('name'),
                logo_url=request.data.get('logo_url'),
                color=request.data.get('color'),
                description=request.data.get('description'),
            )
        
            return CREATED(body=response)
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