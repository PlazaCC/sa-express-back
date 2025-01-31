import time
import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.infra.repositories.repository import Repository

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            requested_user = AuthAuthorizerDTO(**request.data.get('requester_user'))

            if requested_user.role != ROLE.ADMIN:
                raise ForbiddenAction('Usuário não autorizado')

            name = request.data.get('name')
            phone = request.data.get('phone')
            role = request.data.get('role')
            user_status = request.data.get('user_status')
            email_verified = request.data.get('email_verified')
            enabled = request.data.get('enabled')

            response = Usecase().execute(
                email=request.data.get('email'),
                name=name,
                phone=phone,
                role=role,
                user_status=user_status,
                email_verified=email_verified,
                enabled=enabled
            )
            return OK(body=response)

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
        self.auth_repo = self.repository.auth_repo

    def execute(self, email: str, name: str = None, phone: str = None, role: str = None, user_status: str = None, email_verified: bool = None, enabled: bool = None) -> dict:
        try:
            user = self.auth_repo.get_user_by_email(email)
            if not user:
                raise EntityError("Usuário não encontrado")

            attributes_to_update = {}

            if name:
                attributes_to_update['name'] = name
            if phone:
                attributes_to_update['phone'] = phone
            if role:
                attributes_to_update['role'] = role
            if user_status:
                attributes_to_update['user_status'] = user_status

            user.updated_at = int(time.time() * 1000)

            updated_user = self.auth_repo.update_user(
                email=email,
                attributes_to_update=attributes_to_update,
                enabled=enabled
            )
            return updated_user.to_dict()

        except EntityError as error:
            raise EntityError('Erro ao atualizar o usuário')


def lambda_handler(event, context):
    http_request = LambdaHttpRequest(event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()
