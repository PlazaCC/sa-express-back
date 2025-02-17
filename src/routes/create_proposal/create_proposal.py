import time
from src.shared.domain.entities.deal_proposal import DealProposal
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS
from src.shared.domain.enums.proposal_type_enum import PROPOSAL_TYPE
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Created, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.infra.repositories.repository import Repository
import uuid

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:         
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')
            
            requester_user = request.data.get('requester_user')

            proposal_type = request.data.get('proposal_type')

            if proposal_type is None:
                raise MissingParameters('proposal_type')
            
            if proposal_type not in PROPOSAL_TYPE._member_names_:
                raise EntityError('proposal_type inválido')
            
            response = Usecase().execute(proposal_type=proposal_type, user_id=requester_user.user_id, **request.data)
            
            return Created(body=response)
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
        self.repository = Repository(proposal_repo=True, deal_repo=True, entity_repo=True)
        self.proposal_repo = self.repository.proposal_repo
        self.deal_repo = self.repository.deal_repo
        self.entity_repo = self.repository.entity_repo
        
    def execute(self, proposal_type: PROPOSAL_TYPE, user_id: str, **kwargs) -> dict:
        if proposal_type == PROPOSAL_TYPE.DEAL:

            deal = self.deal_repo.get_deal_by_id(
                entity_id=kwargs.get('entity_id'),
                deal_id=kwargs.get('deal_id'),
                status=DEAL_STATUS.ACTIVATED.value
            )

            if deal is None:
                raise EntityError('Acordo não existe ou está inativo')

            proposal = DealProposal(
                proposal_id=str(uuid.uuid4()),
                user_id=user_id,
                proposal_type=proposal_type,
                status=PROPOSAL_STATUS.PENDING,
                created_at=int(round(time.time() * 1000)),
                updated_at=int(round(time.time() * 1000)),
                deal_id=kwargs.get('deal_id'),
                entity_id=kwargs.get('entity_id')
            )
        else:
            raise EntityError('Proposta inválida')
        
        proposal_created = self.proposal_repo.create_proposal(proposal)

        return proposal_created.to_dict()

def function_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()