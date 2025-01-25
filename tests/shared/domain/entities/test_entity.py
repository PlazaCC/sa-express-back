import pytest
from src.shared.domain.entities.entity import Entity
from src.shared.helpers.errors.errors import EntityError


class Test_Entity:
  
  def test_entity(self):
    entity = Entity(
      entity_id="00000000-0000-0000-0000-000000000000",
      registers=1,
      ftds=1,
      rev_share=1,
      costs_per_acquisition=1,
      shipping_volume=1,
      base_quality=1,
      commission_total_paid=1,
      average_deposit=1,
      operators_satisfaction=1,
      created_at=1,
      updated_at=1
    )
    
    assert entity.entity_id == "00000000-0000-0000-0000-000000000000"
    assert entity.registers == 1
    assert entity.ftds == 1
    assert entity.rev_share == 1
    assert entity.costs_per_acquisition == 1
    assert entity.shipping_volume == 1
    assert entity.base_quality == 1
    assert entity.commission_total_paid == 1
    assert entity.average_deposit == 1
    assert entity.operators_satisfaction == 1
    assert entity.created_at == 1
    assert entity.updated_at == 1
    
  # def test_entity_id_not_string(self):
  #   with pytest.raises(EntityError):
  #     Entity(
  #       entity_id=1,
  #       registers=1,
  #       ftds=1,
  #       rev_share=1,
  #       costs_per_acquisition=1,
  #       shipping_volume=1,
  #       base_quality=1,
  #       commission_total_paid=1,
  #       average_deposit=1,
  #       operators_satisfaction=1
  #     )