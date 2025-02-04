from src.shared.domain.entities.entity import Entity
from src.shared.infra.repositories.mocks.entity_repository_mock import EntityRepositoryMock


class Test_EntityRepositoryMock:
  
  def test_create_entity(self):
    repo = EntityRepositoryMock()
    
    entity = Entity(
        entity_id="00000000-0000-0000-0000-000000000003",
        average_deposit=4,
        base_quality=4,
        commission_total_paid=4,
        costs_per_acquisition=4,
        ftds=4,
        operators_satisfaction=4,
        registers=4,
        rev_share=4,
        shipping_volume=4,
        created_at=1,
        updated_at=1
      )
    
    repo.create_entity(entity)
    
    assert repo.entities[3].entity_id == "00000000-0000-0000-0000-000000000003"
    assert len(repo.entities) == 4
    
  def test_get_entity_by_id(self):
    repo = EntityRepositoryMock()
    
    entity = repo.get_entity_by_id("00000000-0000-0000-0000-000000000001")
    
    assert entity.entity_id == "00000000-0000-0000-0000-000000000001"
    
  def test_get_entity_by_id_not_found(self):
    repo = EntityRepositoryMock()
    
    entity = repo.get_entity_by_id("00000000-0000-0000-0000-000000000004")
    
    assert entity == None
    
    