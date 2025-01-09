from curses import OK
from datetime import time
import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.dtos.user_api_gateway_dto import UserApiGatewayDTO
from src.shared.infra.repositories.repository import Repository


class  Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            requested_user = UserApiGatewayDTO(**request.data.get('requester_user'))
            
            if requested_user.role != ROLE.ADMIN:
                raise ForbiddenAction('Usuário não autorizado')
            
            if request.data.get('name') is None:
                raise MissingParameters('name')
            
            if request.data.get('email') is None:
                raise MissingParameters('email')
            
            if request.data.get('phone') is None:
                raise MissingParameters('phone')
            
            if request.data.get('role') is None:
                raise MissingParameters('role')
            
            response = Usecase().execute(
                name=request.data.get('name'),
                email=request.data.get('email'),
                phone=request.data.get('phone'),
                role=request.data.get('role')
            )
            return OK(body=response)\
            
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return Forbidden(error.message)
        except EntityError as error:
            return BadRequest(error.message)
        except Exception as error:
            return InternalServerError(str(error))
        

class Usecase:
    repository: Repository
    
    def __init__(self):
        self.repository = Repository(auth_repo=True)
        self.repository = self.repository.auth_repo
        
    def execute(self, name: str, email: str, phone: str, role: ROLE):
        user = User(
            user_id=uuid.uuid4(), 
            name=name,
            email=email,
            phone=phone,
            role=role,
            user_status=USER_STATUS.UNKNOWN,
            created_at=int(round(time.time()*1000)),            
            updated_at=int(round(time.time()*1000)),
            email_verified=False,
            enabled=True
        )
        
        user_created = self.repository.create_user(user)
        return user_created.to_dict()
    
    def function_handler(event, context):
        http_request = LambdaHttpRequest(event)
        http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
        response = Controller.execute(http_request)
        http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
        
        return http_response.toDict()