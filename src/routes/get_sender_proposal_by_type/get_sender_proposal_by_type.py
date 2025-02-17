from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS
from src.shared.domain.enums.proposal_type_enum import PROPOSAL_TYPE
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
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')
            
            requester_user = request.data.get('requester_user')

            proposal_type = request.data.get('proposal_type')
            status = request.data.get('status')

            if proposal_type is None:
                raise MissingParameters('proposal_type')
            
            if status is None:
                raise MissingParameters('status')
            
            if proposal_type not in PROPOSAL_TYPE._member_names_:
                raise EntityError('proposal_type inválido')
            
            if status not in PROPOSAL_STATUS._member_names_:
                raise EntityError('status inválido')
            
            response = Usecase().execute(user_id=requester_user.user_id, proposal_type=proposal_type, status=status)
            return OK(body=response)
        
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return Forbidden(error.message)
        except EntityError as error:
            return BadRequest(error.message)
        except ValueError as error:
            return BadRequest(error.args[0])
        except Exception as error:
            return InternalServerError(str(error))

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