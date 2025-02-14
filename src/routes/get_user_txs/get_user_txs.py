from src.shared.domain.entities.tx import TX
from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            requester_user = AuthAuthorizerDTO.from_api_gateway(request.data.get('requester_user'))

            ini_timestamp=None
            end_timestamp=None
            last_evaluated_key = None

            if request.data.get('ini_timestamp') is not None:
                ini_timestamp = int(request.data.get('ini_timestamp'))

            if request.data.get('end_timestamp') is not None:
                end_timestamp = int(request.data.get('end_timestamp'))

            if request.data.get('last_evaluated_key') is not None:
                last_evaluated_key = request.data.get('last_evaluated_key')

            response = Usecase().execute(requester_user, ini_timestamp, \
                end_timestamp, last_evaluated_key)
            
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except Exception as _:
            return InternalServerError('Erro interno de servidor')
        
class Usecase:
    repository: Repository
    wallet_repo: IWalletRepository

    def __init__(self):
        self.repository = Repository(wallet_repo=True)

        self.wallet_repo = self.repository.wallet_repo

    def execute(self, requester_user: AuthAuthorizerDTO, ini_timestamp: int | None, end_timestamp: int | None, \
        last_evaluated_key: str | None) -> dict:
        resp = self.wallet_repo.get_transactions_by_user(
            user=requester_user,
            limit=20,
            ini_timestamp=ini_timestamp,
            end_timestamp=end_timestamp,
            last_evaluated_key=last_evaluated_key,
        )

        return {
            'txs': [ tx.to_user_public() for tx in resp['txs'] ],
            'last_evaluated_key': resp['last_evaluated_key']
        }

def lambda_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)

    http_request.data['requester_user'] = event.get('requestContext', {}) \
        .get('authorizer', {}) \
        .get('claims', None)
    
    response = Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()