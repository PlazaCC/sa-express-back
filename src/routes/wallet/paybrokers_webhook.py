from src.shared.infra.repositories.repository import Repository
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters

from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.mocks.wallet_paygate_mock import WalletPayGateMock
from src.shared.wallet.tx_results.pop import TXPopResult

class Controller:
    @staticmethod
    async def execute(request: IRequest) -> IResponse:
        try:
            if 'PAYGATE_AUTH' not in request.headers:
                raise MissingParameters('PAYGATE_AUTH')
            
            webhook_auth_header = request.headers.get('PAYGATE_AUTH')

            response = await Usecase().execute(webhook_auth_header)

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
    
    async def execute(self, webhook_auth_header: str) -> dict:
        tx = self.tx_proc.get_tx_from_webhook(webhook_auth_header)

        if tx is None:
            return {}

        async def pop_callback(pop_result: TXPopResult):
            pass
        
        await self.tx_proc.pop_tx_with_callback(pop_callback, tx)

        return {}
        
async def function_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)
    
    response = await Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()