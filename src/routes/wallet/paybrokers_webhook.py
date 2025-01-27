import json
import hmac
import hashlib

from src.environments import Environments

from src.shared.infra.repositories.repository import Repository
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest, Forbidden
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.mocks.wallet_paygate_mock import WalletPayGateMock
from src.shared.wallet.tx_results.pop import TXPopResult

class Controller:
    @staticmethod
    async def execute(request: IRequest) -> IResponse:
        try:
            if 'X-Webhook-Signature' not in request.headers:
                raise MissingParameters('X-Webhook-Signature')

            if 'X-Webhook-Reference' not in request.headers:
                raise MissingParameters('X-Webhook-Reference')
            
            body = request.body
            
            if 'id' not in body:
                raise MissingParameters('id')
            
            if 'transactionState' not in body:
                raise MissingParameters('transactionState')
            
            webhook_sig_header = request.headers['X-Webhook-Signature']
            webhook_ref_header = request.headers.get('X-Webhook-Reference')
            
            usecase = Usecase()

            if usecase.verify_signature(webhook_sig_header, body):
                raise ForbiddenAction('Verificação do sig-header falhou')

            response = await usecase.execute(webhook_ref_header)

            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return Forbidden(error.message)
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

    def parse_sig_header(self, webhook_sig_header: str) -> dict | None:
        try:
            header_split = webhook_sig_header.split('HMAC-SHA256')

            if len(header_split) != 2:
                return None
            
            header_fields = header_split.pop()
            header_fields = header_fields.split(',')

            if len(header_fields) != 3:
                return None

            result = {}

            for raw_field in header_fields:
                (key, value) = raw_field.strip().split('=')
                
                result[key] = value

            if 'Sign' not in result:
                return None
            
            if 'Nonce' not in result:
                return None
            
            if 'TS' not in result:
                return None

            return result
        except:
            return None

    def verify_signature(self, webhook_sig_header: str, body: dict) -> bool:
        sig_params = self.parse_sig_header(webhook_sig_header)

        if sig_params is None:
            return True
        
        try:
            message = sig_params['Nonce'] + ':' + sig_params['TS'] + ':' + json.dumps(body, separators=(',', ':'))
        except:
            return True
        


        print(message)
        
        return False
    
    async def execute(self, webhook_ref_header: str) -> dict:
        tx = self.tx_proc.get_tx_from_webhook(webhook_ref_header)

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