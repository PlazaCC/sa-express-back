import pytest
from src.shared.domain.entities.affiliation import Affiliation


class Test_Affiliation:
  
  def test_affiliation(self):
    affiliation = Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        cost_per_acquisition=1,
        base_quality=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
    )
    
    assert affiliation.affiliation_id == "00000000-0000-0000-0000-000000000000"
    assert affiliation.deal_id == "00000000-0000-0000-0000-000000000000"
    assert affiliation.user_id == "00000000-0000-0000-0000-000000000000"
    assert affiliation.amount_to_pay == 1
    assert affiliation.baseline == 1
    assert affiliation.commission == 1
    assert affiliation.base_quality == 1
    assert affiliation.cost_per_acquisition == 1
    assert affiliation.ftd == 1
    assert affiliation.invoiced_amount == 1
    assert affiliation.operators_satisfaction == 1
    assert affiliation.registers == 1
    assert affiliation.rev_share == 1
    assert affiliation.shipping_volume == 1
    
  def test_affiliation_id_not_string(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id=1,
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        cost_per_acquisition=1,
        base_quality=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_affiliation_id_not_36_characters(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="1",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        cost_per_acquisition=1,
        ftd=1,
        base_quality=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_deal_id_not_string(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id=1,
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        cost_per_acquisition=1,
        base_quality=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_deal_id_not_36_characters(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="1",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        base_quality=1,
        cost_per_acquisition=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_user_id_not_string(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id=1,
        amount_to_pay=1,
        baseline=1,
        commission=1,
        base_quality=1,
        cost_per_acquisition=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_user_id_not_36_characters(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="1",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        cost_per_acquisition=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        base_quality=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_amount_to_pay_not_float(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay="not_a_float",
        baseline=1,
        commission=1,
        cost_per_acquisition=1,
        base_quality=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_baseline_not_float(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline="not_a_float",
        commission=1,
        cost_per_acquisition=1,
        ftd=1,
        base_quality=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_commission_not_float(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission="not_a_float",
        cost_per_acquisition=1,
        base_quality=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_cost_per_acquisition_not_int(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        base_quality=1,
        cost_per_acquisition="not_an_int",
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_ftd_not_int(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        base_quality=1,
        cost_per_acquisition=1,
        ftd="not_an_int",
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_invoiced_amount_not_float(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        base_quality=1,
        cost_per_acquisition=1,
        ftd=1,
        invoiced_amount="not_a_float",
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_operators_satisfaction_not_float(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        cost_per_acquisition=1,
        base_quality=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction="not_a_float",
        registers=1,
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_registers_not_int(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        base_quality=1,
        cost_per_acquisition=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers="not_an_int",
        rev_share=1,
        shipping_volume=1,
      )
      
  def test_rev_share_not_float(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        cost_per_acquisition=1,
        ftd=1,
        base_quality=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share="not_a_float",
        shipping_volume=1,
      )
      
  def test_shipping_volume_not_float(self):
    with pytest.raises(ValueError):
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-000-0000-0000-000000000000",
        user_id="00000000-0000-000-0000-000000000000",
        amount_to_pay=1,
        baseline=1,
        commission=1,
        base_quality=1,
        cost_per_acquisition=1,
        ftd=1,
        invoiced_amount=1,
        operators_satisfaction=1,
        registers=1,
        rev_share=1,
        shipping_volume="not_a_float",
      )