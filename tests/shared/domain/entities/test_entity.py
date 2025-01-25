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
    
  def test_entity_id_not_string(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id=1,
        registers=1,
        ftds=1,
        rev_share=1,
        costs_per_acquisition=1,
        shipping_volume=1,
        base_quality=1,
        commission_total_paid=1,
        average_deposit=1,
        operators_satisfaction=1
      )
      
  def test_entity_id_not_36_characters(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="1",
        registers=1,
        ftds=1,
        rev_share=1,
        costs_per_acquisition=1,
        shipping_volume=1,
        base_quality=1,
        commission_total_paid=1,
        average_deposit=1,
        operators_satisfaction=1
      )
      
  def test_registers_not_integer(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        registers="not_an_int",
        ftds=1,
        rev_share=1,
        costs_per_acquisition=1,
        shipping_volume=1,
        base_quality=1,
        commission_total_paid=1,
        average_deposit=1,
        operators_satisfaction=1
      )
      
  def test_ftds_not_integer(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        registers=1,
        ftds="not_an_int",
        rev_share=1,
        costs_per_acquisition=1,
        shipping_volume=1,
        base_quality=1,
        commission_total_paid=1,
        average_deposit=1,
        operators_satisfaction=1
      )
      
  def test_rev_share_not_float(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        registers=1,
        ftds=1,
        rev_share="not_a_float",
        costs_per_acquisition=1,
        shipping_volume=1,
        base_quality=1,
        commission_total_paid=1,
        average_deposit=1,
        operators_satisfaction=1
      )
      
  def test_costs_per_acquisition_not_float(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        registers=1,
        ftds=1,
        rev_share=1,
        costs_per_acquisition="not_a_float",
        shipping_volume=1,
        base_quality=1,
        commission_total_paid=1,
        average_deposit=1,
        operators_satisfaction=1
      )
      
  def test_shipping_volume_not_float(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        registers=1,
        ftds=1,
        rev_share=1,
        costs_per_acquisition=1,
        shipping_volume="not_a_float",
        base_quality=1,
        commission_total_paid=1,
        average_deposit=1,
        operators_satisfaction=1
      )
      
  def test_base_quality_not_float(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        registers=1,
        ftds=1,
        rev_share=1,
        costs_per_acquisition=1,
        shipping_volume=1,
        base_quality="not_a_float",
        commission_total_paid=1,
        average_deposit=1,
        operators_satisfaction=1
      )
      
  def test_commission_total_paid_not_float(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        registers=1,
        ftds=1,
        rev_share=1,
        costs_per_acquisition=1,
        shipping_volume=1,
        base_quality=1,
        commission_total_paid="not_a_float",
        average_deposit=1,
        operators_satisfaction=1
      )
      
  def test_average_deposit_not_float(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        registers=1,
        ftds=1,
        rev_share=1,
        costs_per_acquisition=1,
        shipping_volume=1,
        base_quality=1,
        commission_total_paid=1,
        average_deposit="not_a_float",
        operators_satisfaction=1
      )
      
  def test_operators_satisfaction_not_float(self):
    with pytest.raises(ValueError):
      Entity(
        entity_id="00000000-0000-0000-0000-000000000000",
        registers=1,
        ftds=1,
        rev_share=1,
        costs_per_acquisition=1,
        shipping_volume=1,
        base_quality=1,
        commission_total_paid=1,
        average_deposit=1,
        operators_satisfaction="not_a_float"
      )
      
  def test_created_at_not_integer(self):
    with pytest.raises(ValueError):
      Entity(
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
        created_at="not_an_int",
        updated_at=1
      )
      
  def test_updated_at_not_integer(self):
    with pytest.raises(ValueError):
      Entity(
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
        updated_at="not_an_int"
      )
      
  def test_created_at_negative(self):
    with pytest.raises(ValueError):
      Entity(
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
        created_at=-1,
        updated_at=1
      )
      
  def test_updated_at_negative(self):
    with pytest.raises(ValueError):
      Entity(
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
        updated_at=-1
      )
      