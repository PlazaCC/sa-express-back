from abc import ABC, abstractmethod

from src.shared.domain.entities.entity import Entity

class IEntityRepository(ABC):

    @abstractmethod
    def get_entity_by_id(self, user_id: str) -> Entity:
        pass
    
    @abstractmethod
    def create_entity(self, entity: Entity) -> Entity:
        pass