from abc import ABC, abstractmethod

from src.shared.domain.entities.deal import Deal


class IDealRepository(ABC): 
    @abstractmethod
    def create_deal(self, deal: Deal) -> Deal:
        pass

    @abstractmethod
    def get_entity_deals(self, entity_id: str, status: str = None, limit: int = 10, last_evaluated_key: str = None):
        pass

    @abstractmethod
    def update_deal_status(self, deal: Deal, new_status: str) -> Deal:
        pass