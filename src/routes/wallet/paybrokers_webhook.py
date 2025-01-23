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
            if 'paygate_ref' not in request.query_params:
                raise MissingParameters('paygate_ref')
            
            paygate_ref = request.query_params.get('paygate_ref')

            response = await Usecase().execute(paygate_ref)

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
                max_vaults=2,
                max_instructions=1,
                tx_queue_type=TX_QUEUE_TYPE.CLIENT
            )
        )
    
    async def execute(self, paygate_ref: str) -> dict:
        (tx, instr_index) = self.tx_proc.get_tx_by_paygate_ref(paygate_ref)

        if tx is None or instr_index is None:
            return {}

        async def pop_callback(pop_result: TXPopResult):
            pass
        
        await self.tx_proc.pop_tx_with_callback(pop_callback, tx, instr_index)

        return {}
        
async def function_handler(event, context) -> LambdaHttpResponse:
    pass