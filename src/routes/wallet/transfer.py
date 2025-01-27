from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.user_api_gateway_dto import UserApiGatewayDTO
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters

from src.shared.wallet.decimal import not_decimal
from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.mocks.wallet_paygate_mock import WalletPayGateMock
from src.shared.wallet.tx_templates.transfer import create_transfer_tx

class Controller:
    @staticmethod
    async def execute(request: IRequest) -> IResponse:
        try:
            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            usecase = Usecase()
            
            src_user_vault = usecase.get_src_user_vault(requester_user)

            if src_user_vault is None:
                return BadRequest('Usuário origem não possui uma carteira')
            
            if 'dst_user_email' not in request.data:
                raise MissingParameters('dst_user_email')
            
            if 'amount' not in request.data:
                raise MissingParameters('amount')
            
            (dst_error, dst_user_vault) = usecase.get_dst_user_vault(request)

            if dst_error != '':
                return BadRequest(dst_error)
            
            amount = request.data.get('amount')
            
            if not_decimal(amount):
                return BadRequest('Valor de transferência inválido')
            
            response = await usecase.execute(requester_user, src_user_vault, dst_user_vault, amount)

            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except Exception as _:
            return InternalServerError('Erro interno de servidor')
        
class Usecase:
    repository: Repository
    wallet_repo: IWalletRepository
    wallet_cache: IWalletCache
    tx_proc: TXProcessor

    def __init__(self):
        self.repository = Repository(wallet_repo=True, wallet_cache=True)

        self.wallet_repo = self.repository.wallet_repo
        self.wallet_cache = self.repository.wallet_cache

        self.tx_proc = TXProcessor(
            cache=self.wallet_cache,
            repository=self.wallet_repo,
            paygate=WalletPayGateMock(),
            config=TXProcessorConfig(
                tx_queue_type=TX_QUEUE_TYPE.CLIENT
            )
        )

    def get_src_user_vault(self, requester_user: UserApiGatewayDTO) -> Vault | None:
        return self.tx_proc.vault_proc.get_by_user(requester_user)
    
    def get_dst_user_vault(self, request: IRequest) -> tuple[str, Vault | None]:
        dst_user_email = request.data.get('dst_user_email')

        if not PIXKey.validate_email(dst_user_email):
            return ('Email do usuário destino inválido', None)
        
        dst_user = self.wallet_repo.get_user_by_email(dst_user_email)
        
        if dst_user is None:
            return ('Usuário destino não foi encontrado', None)
        
        dst_user_vault = self.tx_proc.vault_proc.get_by_user(dst_user)

        if dst_user_vault is None:
            return ('Usuário destino não possui uma carteira', None)

        return ('', dst_user_vault)
    
    async def execute(self, requester_user: UserApiGatewayDTO, src_user_vault: Vault, dst_user_vault: Vault, \
        amount: str) -> dict:
        transfer_tx = create_transfer_tx({ 
            'from_vault': src_user_vault, 
            'to_vault': dst_user_vault,
            'amount': amount
        })

        result = await self.tx_proc.push_tx(requester_user, transfer_tx)
        
        return {
            'tx_id': transfer_tx.tx_id,
            'result': result.to_dict()
        }
        
async def function_handler(event, context) -> LambdaHttpResponse:
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