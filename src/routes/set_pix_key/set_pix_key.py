from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest

from src.shared.wallet.vault_processor import VaultProcessor
from src.shared.wallet.models.pix import PIXKey

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            requester_user = AuthAuthorizerDTO.from_api_gateway(request.data.get('requester_user'))

            pix_key = PIXKey.from_api_gateway(request.data.get('pix_key'))

            if not pix_key.valid():
                return BadRequest('Chave PIX inválida')
            
            response = Usecase().execute(requester_user, pix_key)

            return OK(body=response)
        except Exception as _:
            return InternalServerError('Erro interno de servidor')
        
class Usecase:
    repository: Repository
    vault_proc: VaultProcessor

    def __init__(self):
        self.repository = Repository(wallet_repo=True, wallet_cache=True)
        
        self.vault_proc = VaultProcessor(
            cache=self.repository.wallet_cache, 
            repository=self.repository.wallet_repo
        )
    
    def execute(self, requester_user: AuthAuthorizerDTO, pix_key: PIXKey) -> dict:
        vault = self.vault_proc.create_if_not_exists(requester_user)

        vault.pix_key = pix_key

        self.vault_proc.persist_vault(vault)

        return {}

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