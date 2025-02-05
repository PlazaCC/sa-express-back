from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse

# from src.shared.infra.repositories.repository import Repository
# from src.shared.domain.repositories.wallet_cache_interface import IWalletCache

from src.shared.environments import Environments

import boto3
from pydantic import BaseModel

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            response = Usecase().execute()

            return OK(body=response)
        except Exception as error:
            return InternalServerError(str(error))

class Usecase:
    # repository: Repository
    # wallet_cache: IWalletCache

    def __init__(self):
        # self.repository = Repository(wallet_cache=True)

        # self.wallet_cache = self.repository.wallet_cache
        pass
    
    def execute(self) -> dict:
        client = boto3.client('elasticache')

        response = client.describe_cache_clusters(ShowCacheNodeInfo=True)

        return response

def lambda_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)

    response = Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()