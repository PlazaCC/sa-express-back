from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache

from src.shared.environments import Environments

import boto3
import pydantic

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            response = Usecase().execute()

            return OK(body=response)
        except Exception as error:
            return InternalServerError('ERROR: ' + str(error))
        
class Usecase:
    repository: Repository
    wallet_repo: IWalletRepository
    wallet_cache: IWalletCache

    def __init__(self):
        self.repository = Repository(wallet_repo=True, wallet_cache=True)

        self.wallet_repo = self.repository.wallet_repo
        self.wallet_cache = self.repository.wallet_cache
    
    def execute(self) -> dict:
        client = boto3.client('elasticache')

        # TODO: give lambda redis-cluster access
        response = client.describe_cache_clusters(ShowCacheNodeInfo=True)

        # rep_vault = self.wallet_repo.get_vault_by_user_id(0)

        # print('rep_vault', rep_vault)

        # return { 'pydantic_version': pydantic.__version__ }
        return response

def lambda_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)

    response = Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()