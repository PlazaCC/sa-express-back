
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.dtos.user_api_gateway_dto import UserApiGatewayDTO
from src.shared.infra.repositories.repository import Repository


class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')
            
            requested_user = UserApiGatewayDTO(**request.data.get('requester_user'))
            
            if requested_user.role != ROLE.ADMIN:
                raise ForbiddenAction('Usuário não autorizado')
            
            requester_user = request.data.get('requester_user')
            
            response = Usecase().execute()
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
        self.repository = Repository(auth_repo=True)
        self.auth_repo = self.repository.auth_repo

    def execute(self) -> dict:
        users = self.auth_repo.get_all_users()
        return [user.to_dict() for user in users]

def function_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()