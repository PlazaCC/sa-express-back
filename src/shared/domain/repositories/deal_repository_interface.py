from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.deal import Deal

class IDealRepository(ABC):

    @abstractmethod
    def create_deal(self, deal: Deal) -> Deal:
        pass

    @abstractmethod
    def get_deal_by_id(self, bet_id: str, deal_id: str) -> Deal:
        pass

    @abstractmethod
    def get_all_active_deals(self) -> List[Deal]:
        pass

    @abstractmethod
    def get_all_deals(self) -> List[Deal]:
        pass

    @abstractmethod
    def update_deal(self, deal_id: str, new_deal: Deal) -> Deal:
        pass

    @abstractmethod
    def delete_deal(self, bet_id: str, deal_id: str) -> Deal:
        pass