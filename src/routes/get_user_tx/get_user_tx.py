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

            if 'tx_id' not in request.query_params:
                raise MissingParameters('tx_id')
            
            tx_id = request.query_params.get('tx_id')

            if TX.invalid_tx_id(tx_id):
                return BadRequest('ID de transação inválido')

            response = Usecase().execute(requester_user, tx_id)
            
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

    def execute(self, requester_user: AuthAuthorizerDTO, tx_id: str) -> dict:
        rep_tx = self.wallet_repo.get_transaction(tx_id)

        if rep_tx is None:
            return {}
        
        if rep_tx.user_id is None or rep_tx.user_id != int(requester_user.user_id):
            return {}

        return {
            'tx': rep_tx.to_user_public()
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