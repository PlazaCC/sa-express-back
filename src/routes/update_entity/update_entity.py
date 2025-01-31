from http.client import CREATED, OK
import time
from src.shared.domain.entities.entity import Banner, Entity
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
    
    def execute(self, entity_id: str, name: str = None, logo_url: str = None, color: str = None, description: str = None) -> dict:
        entity = self.entity_repo.get_entity(entity_id)

        if entity is None:
            raise NoItemsFound('Entity not found')
        
        if name is None and logo_url is None and color is None and description is None:
            raise MissingParameters('name or logo_url or color or description')
        
        if name is not None:
            entity.name = name
        
        if logo_url is not None:
            entity.banner.logo_url = logo_url
        
        if color is not None:
            entity.banner.color = color
        
        if description is not None:
            entity.description = description

        entity.updated_at = int(round(time.time() * 1000))

        entity_updated = self.entity_repo.update_entity(entity)

        return entity_updated.to_dict()

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
                entity_id=request.data.get('entity_id'),
                name=request.data.get('name'),
                logo_url=request.data.get('logo_url'),
                color=request.data.get('color'),
                description=request.data.get('description'),
            )
        
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return Forbidden(error.message)
        except EntityError as error:
            return BadRequest(error.message)
        except ValueError as error:
            return BadRequest({"validation_errors": error.errors()})
        except Exception as error:
            return InternalServerError(str(error))

def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()