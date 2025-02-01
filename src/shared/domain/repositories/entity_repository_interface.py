from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.deal import Deal
from src.shared.domain.entities.entity import Entity


class IEntityRepository(ABC):

    @abstractmethod
    def get_entity(self, entity_id: str) -> Entity:
        pass

    @abstractmethod
    def create_entity(self, entity: Entity) -> Entity:
        pass

    @abstractmethod
    def update_entity(self, new_entity: Entity) -> Entity:
        pass

    @abstractmethod
    def get_all_entities(self) -> List[Entity]:
        pass

    @abstractmethod
    def create_deal(self, deal: Deal) -> Deal:
        pass

    @abstractmethod
    def get_entity_deals(self, entity_id: str, status: str = None, limit: int = 10, last_evaluated_key: str = None):
        pass

    @abstractmethod
    def update_deal_status(self, deal: Deal, new_status: str) -> Deal:
        pass