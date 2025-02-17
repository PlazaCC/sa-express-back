from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache
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
            
            pix_key = None

            if 'pix_key' in request.data:
                pix_key = PIXKey.from_api_gateway(request.data.get('pix_key'))

                if not pix_key.valid():
                    return BadRequest('Chave PIX inválida')

            response = Usecase().execute(requester_user, pix_key)

            return OK(body=response)
        except Exception as _:
            return InternalServerError('Erro interno de servidor')
        
class Usecase:
    repository: Repository
    wallet_repo: IWalletRepository
    wallet_cache: IWalletCache
    vault_proc: VaultProcessor

    def __init__(self):
        self.repository = Repository(wallet_repo=True, wallet_cache=True)

        self.wallet_repo = self.repository.wallet_repo
        self.wallet_cache = self.repository.wallet_cache

        self.vault_proc = VaultProcessor(
            cache=self.wallet_cache, 
            repository=self.wallet_repo
        )
    
    def execute(self, requester_user: AuthAuthorizerDTO, pix_key: PIXKey | None) -> dict:
        vault = self.vault_proc.create_if_not_exists(requester_user)

        if pix_key is not None:
            vault.pix_key = pix_key

            self.vault_proc.persist_vault(vault)

        return {
            'vault': vault.to_user_public()
        }

def function_handler(event, context) -> LambdaHttpResponse:
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