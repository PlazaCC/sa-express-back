from typing import List
from src.shared.domain.entities.deal_proposal import DealProposal, Proposal
from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS
from src.shared.domain.repositories.proposal_repository_interface import IProposalRepository
from src.shared.infra.external.key_formatters import profile_primary_key, proposal_gsi_receiver_primary_key, proposal_gsi_receiver_sort_key, proposal_sort_key


class ProposalRepositoryDynamo(IProposalRepository):

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
    
    def get_my_proposal_by_type(self, user_id: str, proposal_type: str, status: PROPOSAL_STATUS) -> List[Proposal]:
        resp = self.dynamo.query(
            partition_key=profile_primary_key(user_id),
            sort_key_prefix=proposal_sort_key(proposal_type, status),
        )
        
        return [Proposal.from_dict(item) for item in resp.get("items", [])]