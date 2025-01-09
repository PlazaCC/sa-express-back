from typing import List

from src.shared.helpers.errors.errors import EntityError


class BetData:
  bet_data_id: str
  registers: int
  ftds: int
  rev_share: float
  costs_per_acquisition: float
  shipping_volume: float
  base_quality: float
  commission_total_paid: float
  average_deposit: float
  operators_satisfaction: float
  
  def __init__(
    self,
    bet_data_id: str,
    registers: int,
    ftds: int,
    rev_share: float,
    costs_per_acquisition: float,
    shipping_volume: float,
    base_quality: float,
    commission_total_paid: float,
    average_deposit: float,
    operators_satisfaction: float
  ):
    self.validator(
      bet_data_id,
      registers,
      ftds,
      rev_share,
      costs_per_acquisition,
      shipping_volume,
      base_quality,
      commission_total_paid,
      average_deposit,
      operators_satisfaction
    )
    
    self.bet_data_id = bet_data_id
    self.registers = registers
    self.ftds = ftds
    self.rev_share = rev_share
    self.costs_per_acquisition = costs_per_acquisition
    self.shipping_volume = shipping_volume
    self.base_quality = base_quality
    self.commission_total_paid = commission_total_paid
    self.average_deposit = average_deposit
    self.operators_satisfaction = operators_satisfaction
    
  def validator(
    self,
    bet_data_id: str,
    registers: int,
    ftds: int,
    rev_share: float,
    costs_per_acquisition: float,
    shipping_volume: float,
    base_quality: float,
    commission_total_paid: float,
    average_deposit: float,
    operators_satisfaction: float
  ):
    if not bet_data_id:
      raise EntityError("Bet Data ID is required")
    if not registers:
      raise EntityError("Registers are required")
    if not ftds:
      raise EntityError("First Time Deposits are required")
    if not rev_share:
      raise EntityError("Revenue Share is required")
    if not costs_per_acquisition:
      raise EntityError("Costs per Acquisition are required")
    if not shipping_volume:
      raise EntityError("Shipping Volume is required")
    if not base_quality:
      raise EntityError("Base Quality is required")
    if not commission_total_paid:
      raise EntityError("Commission Total Paid is required")
    if not average_deposit:
      raise EntityError("Average Deposit is required")
    if not operators_satisfaction:
      raise EntityError("Operators Satisfaction is required")
    return True
  
  
  
  