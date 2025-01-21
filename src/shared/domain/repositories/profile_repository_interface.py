from abc import ABC, abstractmethod

from src.shared.domain.entities.profile import Profile

class IProfileRepository(ABC):

    @abstractmethod
    def get_profile_by_id(self, user_id: str) -> Profile:
        pass
    
    @abstractmethod
    def create_profile(self, profile: Profile) -> Profile:
        pass
    
    @abstractmethod
    def deactivate_profile(self, user_id: str) -> Profile:
        pass

  