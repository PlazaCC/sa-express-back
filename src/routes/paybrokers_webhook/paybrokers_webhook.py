import os
import json
import hmac
import hashlib
import asyncio

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
            headers = request.headers

            if 'X-Webhook-Signature' not in headers:
                raise MissingParameters('X-Webhook-Signature')

            if 'X-Webhook-Reference' not in headers:
                raise MissingParameters('X-Webhook-Reference')
            
            webhook_sig_header = headers.get('X-Webhook-Signature')
            webhook_ref_header = headers.get('X-Webhook-Reference')
            
            webhook_body = request.body
            
            if 'transactionState' not in webhook_body:
                raise MissingParameters('transactionState')
            
            usecase = Usecase()

            if usecase.verify_signature(webhook_sig_header, webhook_body):
                raise ForbiddenAction('Verificação do sig-header falhou')

            response = await usecase.execute(webhook_ref_header, webhook_body)

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

        if 'Sign' not in result or 'Nonce' \
            not in result or 'TS' \
            not in result:
            return None
        
        return result

    def verify_signature(self, webhook_sig_header: str, webhook_body: dict) -> bool:
        sig_params = self.parse_sig_header(webhook_sig_header)

        if sig_params is None:
            return True
        
        message = sig_params['Nonce'] + ':' + sig_params['TS'] + ':' + json.dumps(webhook_body, separators=(',', ':'))
        
        key = os.environ.get('PAYBROKERS_WEBHOOK_KEY').encode('utf8')
        hash = hmac.new(key, message.encode(), hashlib.sha256)

        generated_sig = hash.hexdigest().upper()

        if generated_sig != sig_params['Sign']:
            return True
        
        return False
    
    async def execute(self, webhook_ref_header: str, webhook_body: dict) -> dict:
        tx = self.tx_proc.get_tx_from_webhook(webhook_ref_header)

        if tx is None:
            return {}
        
        deferred = asyncio.get_event_loop().create_future()

        async def pop_callback(pop_result: TXPopResult):
            deferred.set_result(True)
        
        transactionState = webhook_body['transactionState']

        error = None if transactionState == 'Completed' else f'Transação da paybrokers falhou com estado "{transactionState}"'
        
        await self.tx_proc.pop_tx_with_callback(pop_callback, tx, error)

        await deferred

        return {}
        
async def lambda_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)
    
    response = await Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()