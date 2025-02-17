from src.shared.environments import STAGE, Environments
from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters

from src.shared.wallet.decimal import not_decimal
from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.wrappers.paygate import IWalletPayGate
from src.shared.wallet.wrappers.paybrokers import Paybrokers
from src.shared.wallet.mocks.wallet_paygate_mock import WalletPayGateMock
from src.shared.wallet.tx_templates.deposit import create_deposit_tx

class Controller:
    @staticmethod
    async def execute(request: IRequest) -> IResponse:
        try:
            requester_user = AuthAuthorizerDTO.from_api_gateway(request.data.get('requester_user'))

            usecase = Usecase()
            
            user_vault = usecase.get_user_vault(requester_user)

            if user_vault is None:
                return BadRequest('Usuário não possui uma carteira')

            if 'amount' not in request.data:
                raise MissingParameters('amount')

            amount = request.data.get('amount')
            
            if not_decimal(amount):
                return BadRequest('Valor de depósito inválido')

            response = await usecase.execute(requester_user, user_vault, amount)

            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except Exception as _:
            return InternalServerError('Erro interno de servidor')
        
class Usecase:
    repository: Repository
    wallet_repo: IWalletRepository
    wallet_cache: IWalletCache
    wallet_paygate: IWalletPayGate
    tx_proc: TXProcessor

    def __init__(self):
        self.repository = Repository(wallet_repo=True, wallet_cache=True)

        self.wallet_repo = self.repository.wallet_repo
        self.wallet_cache = self.repository.wallet_cache

        if Environments.stage == STAGE.TEST:
            self.wallet_paygate = WalletPayGateMock()
        else:
            self.wallet_paygate = Paybrokers()

        self.tx_proc = TXProcessor(
            cache=self.wallet_cache,
            repository=self.wallet_repo,
            paygate=self.wallet_paygate,
            config=TXProcessorConfig(
                tx_queue_type=TX_QUEUE_TYPE.CLIENT
            )
        )

    def get_user_vault(self, requester_user: AuthAuthorizerDTO) -> Vault | None:
        return self.tx_proc.vault_proc.get_by_user(requester_user)
    
    async def execute(self, requester_user: AuthAuthorizerDTO, user_vault: Vault, amount: str) -> dict:
        deposit_tx = create_deposit_tx({ 'to_vault': user_vault, 'amount': amount })

        result = await self.tx_proc.push_tx(requester_user, deposit_tx)
        
        return {
            'tx_id': deposit_tx.tx_id,
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