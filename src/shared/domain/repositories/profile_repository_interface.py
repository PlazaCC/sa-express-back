from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.entities.deal_proposal import Proposal
from src.shared.domain.entities.profile import Profile
from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS

class IProfileRepository(ABC):

    @abstractmethod
    def get_profile_by_id(self, user_id: str) -> Profile:
        pass
    
    @abstractmethod
    def create_profile(self, profile: Profile) -> Profile:
        pass
    
    @abstractmethod
    def update_profile(self, new_profile: Profile) -> Profile:
        pass
  