from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS
from src.shared.domain.enums.proposal_type_enum import PROPOSAL_TYPE
from src.shared.helpers.errors.errors import EntityError, ForbiddenAction, MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO
from src.shared.infra.repositories.repository import Repository

class Usecase:
    repository: Repository
    
    def __init__(self):
        self.repository = Repository(proposal_repo=True)
        self.proposal_repo = self.repository.proposal_repo
        
    def execute(self, user_id: str, proposal_type: PROPOSAL_TYPE, status: PROPOSAL_STATUS) -> dict:
        proposals = self.proposal_repo.get_my_proposal_by_type_and_status(user_id=user_id, proposal_type=proposal_type, status=status)
        
        return [proposal.to_dict() for proposal in proposals]

def function_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()