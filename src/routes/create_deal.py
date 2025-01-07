
from datetime import time
import uuid
from src.shared.domain.entities.deal import Deal
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.dtos.user_api_gateway_dto import UserApiGatewayDTO
from src.shared.infra.repositories.repository import Repository


class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:         
            requester_user = UserApiGatewayDTO(**request.data.get('requester_user'))

            if requester_user.role != ROLE.OPERADOR:
                raise ForbiddenAction('Usuário não autorizado')

            if request.data.get('bet_id') is None:
                raise MissingParameters('bet_id')
            
            if request.data.get('baseline') is None:
                raise MissingParameters('baseline')
            
            if request.data.get('cpa') is None:
                raise MissingParameters('cpa')
            
            if request.data.get('rev_share') is None:
                raise MissingParameters('rev_share')
            
            if request.data.get('conditions') is None:
                raise MissingParameters('conditions')

            response = Usecase().execute(
                bet_id=request.data.get('bet_id'),
                baseline=request.data.get('baseline'),
                cpa=request.data.get('cpa'),
                rev_share=request.data.get('rev_share'),
                conditions=request.data.get('conditions'),
            )
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return Forbidden(error.message)
        except EntityError as error:
            return BadRequest(error.args[0])
        except ValueError as error:
            return BadRequest(error.args[0])
        except Exception as error:
            return InternalServerError(str(error))

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(deal_repo=True)
        self.deal_repo = self.repository.deal_repo

    def execute(self, bet_id: str, baseline: str, cpa: str, rev_share: str, conditions: str) -> dict:
        deal = Deal(
            deal_id=uuid.uuid4(),
            bet_id=bet_id,
            baseline=float(baseline),
            cpa=float(cpa),
            rev_share=float(rev_share),
            conditions=conditions,
            deal_status=DEAL_STATUS.ACTIVATED,
            created_at=int(round(time.time() * 1000)),
            updated_at=int(round(time.time() * 1000)),
        )

        deal_created = self.deal_repo.create_deal(deal)

        return deal_created.to_dict()

def function_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()