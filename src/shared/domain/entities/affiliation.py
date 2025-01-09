from typing import List

from src.shared.helpers.errors.errors import EntityError


class Affiliation:
  affiliation_id: str
  invoiced_amount: float
  amount_to_pay: float
  commission: float
  baseline: float
  cost_per_acquisition: int
  rev_share: float
  registers: int
  ftd: int
  shipping_volume: float
  base_quality: float
  operators_satisfaction: float
  
  def __init__(
    self,
    affiliation_id: str,
    invoiced_amount: float,
    amount_to_pay: float,
    commission: float,
    baseline: float,
    cost_per_acquisition: int,
    rev_share: float,
    registers: int,
    ftd: int,
    shipping_volume: float,
    base_quality: float,
    operators_satisfaction: float
  ):
    self.validator(
      affiliation_id,
      invoiced_amount,
      amount_to_pay,
      commission,
      baseline,
      cost_per_acquisition,
      rev_share,
      registers,
      ftd,
      shipping_volume,
      base_quality,
      operators_satisfaction
    )
    
    self.affiliation_id = affiliation_id
    self.invoiced_amount = invoiced_amount
    self.amount_to_pay = amount_to_pay
    self.commission = commission
    self.baseline = baseline
    self.cost_per_acquisition = cost_per_acquisition
    self.rev_share = rev_share
    self.registers = registers
    self.ftd = ftd
    self.shipping_volume = shipping_volume
    self.base_quality = base_quality
    self.operators_satisfaction = operators_satisfaction
  
  def validator(
    self,
    affiliation_id: str,
    invoiced_amount: float,
    amount_to_pay: float,
    commission: float,
    baseline: float,
    cost_per_acquisition: int,
    rev_share: float,
    registers: int,
    ftd: int,
    shipping_volume: float,
    base_quality: float,
    operators_satisfaction: float
  ):
    if not affiliation_id:
      raise EntityError("Affiliation ID is required")
    if not invoiced_amount:
      raise EntityError("Invoiced amount is required")
    if not amount_to_pay:
      raise EntityError("Amount to pay is required")
    if not commission:
      raise EntityError("Commission is required")
    if not baseline:
      raise EntityError("Baseline is required")
    if not cost_per_acquisition:
      raise EntityError("Cost per acquisition is required")
    if not rev_share:
      raise EntityError("Rev share is required")
    if not registers:
      raise EntityError("Registers is required")
    if not ftd:
      raise EntityError("FTD is required")
    if not shipping_volume:
      raise EntityError("Shipping volume is required")
    if not base_quality:
      raise EntityError("Base quality is required")
    if not operators_satisfaction:
      raise EntityError("Operators satisfaction is required")
    return True