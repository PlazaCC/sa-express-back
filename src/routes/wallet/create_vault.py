from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.user_api_gateway_dto import UserApiGatewayDTO
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError

class Controller:
    @staticmethod
    async def execute(request: IRequest) -> IResponse:
        try:
            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            response = await Usecase().execute(requester_user)

            return OK(body=response)
        except Exception as error:
            return InternalServerError(str(error))
        
class Usecase:
    repository: Repository

    def __init__(self):
        pass

    async def execute(self, requester_user: UserApiGatewayDTO) -> dict:
        return {}

async def function_handler(event, context):
    http_request = LambdaHttpRequest(event)

    http_request.data['requester_user'] = event.get('requestContext', {}) \
        .get('authorizer', {}) \
        .get('claims', None)
    
    response = await Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()