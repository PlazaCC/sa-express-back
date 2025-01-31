
import time
from http.client import CREATED
import uuid
from src.shared.domain.entities.deal import Deal
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.infra.repositories.repository import Repository


class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:         
            # if request.data.get('requester_user') is None:
            #     raise MissingParameters('requester_user')
            
            # requester_user = request.data.get('requester_user')

            # if requester_user.role != ROLE.ADMIN and requester_user.role != ROLE.OPERADOR:
            #     raise ForbiddenAction('Usuário não autorizado')

            if request.data.get('entity_id') is None:
                raise MissingParameters('entity_id')
            
            if request.data.get('baseline') is None:
                raise MissingParameters('baseline')
            
            if request.data.get('cpa') is None:
                raise MissingParameters('cpa')
            
            if request.data.get('rev_share') is None:
                raise MissingParameters('rev_share')
            
            if request.data.get('conditions') is None:
                raise MissingParameters('conditions')

            response = Usecase().execute(
                entity_id=request.data.get('entity_id'),
                baseline=request.data.get('baseline'),
                cpa=request.data.get('cpa'),
                rev_share=request.data.get('rev_share'),
                conditions=request.data.get('conditions'),
            )
            return CREATED(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return Forbidden(error.message)
        except EntityError as error:
            return BadRequest(error.message)
        except ValueError as error:
            return BadRequest({"validation_errors": error.errors()})
        except Exception as error:
            return InternalServerError(str(error))

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(entity_repo=True)
        self.entity_repo = self.repository.entity_repo

    def execute(self, entity_id: str, baseline: str, cpa: str, rev_share: str, conditions: str) -> dict:
        deal = Deal(
            deal_id=uuid.uuid4(),
            entity_id=entity_id,
            baseline=float(baseline),
            cpa=float(cpa),
            rev_share=float(rev_share),
            conditions=conditions,
            deal_status=DEAL_STATUS.ACTIVATED,
            created_at=int(round(time.time() * 1000)),
            updated_at=int(round(time.time() * 1000)),
        )

        deal_created = self.entity_repo.create_deal(deal)

        return deal_created.to_dict()

def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()