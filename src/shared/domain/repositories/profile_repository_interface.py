from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.entities.profile import Profile

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
    
    @abstractmethod
    def get_affiliation_by_id(self, user_id: str) -> Affiliation:
        pass
    
    @abstractmethod
    def create_affiliation(self, affiliation: Affiliation) -> Affiliation:
        pass
    
    @abstractmethod
    def get_all_my_affiliations(self, user_id: str) -> dict:
        pass

  