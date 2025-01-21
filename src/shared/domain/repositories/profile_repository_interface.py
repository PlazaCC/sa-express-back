from abc import ABC, abstractmethod

from src.shared.domain.entities.profile import Profile

class IProfileRepository(ABC):

    @abstractmethod
    def get_profile_by_id(self, user_id: str) -> Profile:
        pass

  