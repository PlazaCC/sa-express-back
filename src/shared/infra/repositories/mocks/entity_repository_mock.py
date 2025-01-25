from typing import List
from src.shared.domain.entities.entity import Entity
from src.shared.domain.repositories.entity_repository_interface import IEntityRepository


class EntityRepositoryMock(IEntityRepository):
  entities: List[Entity]
  
  def __init__(self):
    self.entities = [
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        average_deposit=1,
        base_quality=1,
        commission_total_paid=1,
        costs_per_acquisition=1,
        ftds=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
        created_at=1,
        updated_at=1
      ),
      Entity(
        entity_id="00000000-0000-0000-0000-000000000001",
        average_deposit=2,
        base_quality=2,
        commission_total_paid=2,
        costs_per_acquisition=2,
        ftds=2,
        operators_satisfaction=2,
        registers=2,
        rev_share=2,
        shipping_volume=2,
        created_at=2,
        updated_at=2
      ),
      Entity(
        entity_id="00000000-0000-0000-0000-000000000002",
        average_deposit=3,
        base_quality=3,
        commission_total_paid=3,
        costs_per_acquisition=3,
        ftds=3,
        operators_satisfaction=3,
        registers=3,
        rev_share=3,
        shipping_volume=3,
        created_at=3,
        updated_at=3
      ),
    ]
    
  def get_entity_by_id(self, user_id):
    for entity in self.entities:
      if entity.entity_id == user_id:
        return entity
    return None
  
  def create_entity(self, entity: Entity) -> Entity:
    self.entities.append(entity)
    return entity
    