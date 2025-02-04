from abc import ABC, abstractmethod
from typing import List
from src.shared.domain.entities.deal_proposal import Proposal
from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS


class IProposalRepository(ABC):

    @abstractmethod
    def create_proposal(self, proposal: Proposal) -> Proposal:
        pass

    @abstractmethod
    def get_my_proposal_by_type_and_status(self, user_id: str, proposal_type: str, status: PROPOSAL_STATUS) -> List[Proposal]:
        pass