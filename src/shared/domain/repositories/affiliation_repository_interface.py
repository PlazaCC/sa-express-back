from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.affiliation import Affiliation


class IAffiliationRepository(ABC):

    @abstractmethod
    def get_affiliation_by_id(self, user_id: str) -> Affiliation:
        pass
    
    @abstractmethod
    def create_affiliation(self, affiliation: Affiliation) -> Affiliation:
        pass
    
    @abstractmethod
    def get_all_my_affiliations(self, user_id: str) -> List[Affiliation]:
        pass