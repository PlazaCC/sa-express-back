from typing import List
from src.shared.domain.entities.entity import Banner, Entity
from src.shared.domain.repositories.entity_repository_interface import IEntityRepository


class EntityRepositoryMock(IEntityRepository):
    entities: List[Entity]

    def __init__(self):
        self.entities = [
            Entity(
                entity_id="entity_id_1",
                name="Entity 1",
                banner=Banner(
                    logo_url="https://example.com/logo1.png",
                    color="#FF0000"
                ),
                created_at=0,
                updated_at=0
            ),
        ]

    def get_entity(self, entity_id: str) -> Entity:
        for entity in self.entities:
            if entity.entity_id == entity_id:
                return entity
        return None
    
    def create_entity(self, entity: Entity) -> Entity:
        self.entities.append(entity)
        return entity
    
    def update_entity(self, new_entity: Entity) -> Entity:
        for entity in self.entities:
            if entity.entity_id == new_entity.entity_id:
                entity.name = new_entity.name
                entity.banner = new_entity.banner
                entity.updated_at = new_entity.updated_at
                return entity
        return None
    
    def delete_entity(self, entity_id: str) -> Entity:
        for entity in self.entities:
            if entity.entity_id == entity_id:
                self.entities.remove(entity)
                return entity
        return None

    def get_all_entities(self) -> List[Entity]:
        return self.entities
