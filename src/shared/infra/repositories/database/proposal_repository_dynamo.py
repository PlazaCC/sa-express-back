from typing import List
from src.shared.domain.entities.deal_proposal import DealProposal, Proposal
from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS
from src.shared.domain.enums.proposal_type_enum import PROPOSAL_TYPE
from src.shared.domain.repositories.proposal_repository_interface import IProposalRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.key_formatters import profile_primary_key, proposal_gsi_receiver_primary_key, proposal_gsi_receiver_sort_key, proposal_sort_key


class ProposalRepositoryDynamo(IProposalRepository):

    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create_proposal(self, proposal: Proposal) -> Proposal:
        item = proposal.to_dict()
        item["PK"] = profile_primary_key(proposal.user_id)
        item["SK"] = proposal_sort_key(proposal.proposal_type, proposal.status)
        if type(proposal) == DealProposal:
            item["GSI#RECEIVER"] = proposal_gsi_receiver_primary_key(proposal.proposal_type, proposal.entity_id)
        else:
            raise Exception("Invalid proposal type")
        item["STATUS#created_at"] = proposal_gsi_receiver_sort_key(proposal.status, proposal.created_at)
        
        self.dynamo.put_item(item=item)
        return proposal
    
    def get_my_proposal_by_type(self, user_id: str, proposal_type: PROPOSAL_TYPE, status: PROPOSAL_STATUS) -> List[Proposal]:
        resp = self.dynamo.query(
            partition_key=profile_primary_key(user_id),
            sort_key_prefix=proposal_sort_key(proposal_type, status),
        )

        if proposal_type == PROPOSAL_TYPE.DEAL:
            return [DealProposal.from_dict(item) for item in resp.get("items", [])]
        
        raise Exception("Invalid proposal type")
    
    def update_proposal_status(self, proposal: Proposal, new_status: PROPOSAL_STATUS) -> Proposal:
        self.dynamo.delete_item(
            partition_key=profile_primary_key(proposal.user_id),
            sort_key=proposal_sort_key(proposal.proposal_type, proposal.status)
        )

        proposal_data = proposal.to_dict()
        proposal_data["status"] = new_status.value
        proposal_data["SK"] = proposal_sort_key(proposal.proposal_type, new_status)
        proposal_data["STATUS#created_at"] = proposal_gsi_receiver_sort_key(new_status, proposal.created_at)

        if isinstance(proposal, DealProposal):
            proposal_data["GSI#RECEIVER"] = proposal_gsi_receiver_primary_key(proposal.proposal_type, proposal.entity_id)
        else:
            raise Exception("Invalid proposal type")

        self.dynamo.put_item(item=proposal_data)

        proposal.status = new_status

        return proposal
