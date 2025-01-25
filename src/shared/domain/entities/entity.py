from typing import Any, List

from pydantic import Field, field_validator

from src.shared.helpers.errors.errors import EntityError


class Entity:
  entity_id: str = Field(..., description="String with 32 characters")
  registers: int
  ftds: int
  rev_share: float
  costs_per_acquisition: float
  shipping_volume: float
  base_quality: float
  commission_total_paid: float
  average_deposit: float
  operators_satisfaction: float
  created_at: int = Field(..., description="Timestamp in seconds")
  updated_at: int = Field(..., description="Timestamp in seconds")
  
  def __init__(
    self,
    entity_id: str,
    registers: int,
    ftds: int,
    rev_share: float,
    costs_per_acquisition: float,
    shipping_volume: float,
    base_quality: float,
    commission_total_paid: float,
    average_deposit: float,
    operators_satisfaction: float,
    created_at: int,
    updated_at: int
  ):
    self.validator(
      entity_id,
      registers,
      ftds,
      rev_share,
      costs_per_acquisition,
      shipping_volume,
      base_quality,
      commission_total_paid,
      average_deposit,
      operators_satisfaction,
      created_at,
      updated_at
    )
    
    self.entity_id = entity_id
    self.registers = registers
    self.ftds = ftds
    self.rev_share = rev_share
    self.costs_per_acquisition = costs_per_acquisition
    self.shipping_volume = shipping_volume
    self.base_quality = base_quality
    self.commission_total_paid = commission_total_paid
    self.average_deposit = average_deposit
    self.operators_satisfaction = operators_satisfaction
    self.created_at = created_at
    self.updated_at = updated_at
    
  @field_validator('entity_id')
  @staticmethod
  def validate_uuid(value: str) -> str:
      if not isinstance(value, str):
          raise EntityError
      if len(value) != 36:
          raise ValueError("uuids must have exactly 36 characters")
      return value
    
  @field_validator('created_at', 'updated_at')
  @staticmethod
  def validate_timestamp(value: Any) -> int:
      if not isinstance(value, int):
          raise EntityError("created_at e updated_at devem ser inteiros representando timestamps")
      if value < 0:
          raise EntityError("Timestamps devem ser inteiros positivos")
      return value
    
  def validator(
    self,
    entity_id: str,
    registers: int,
    ftds: int,
    rev_share: float,
    costs_per_acquisition: float,
    shipping_volume: float,
    base_quality: float,
    commission_total_paid: float,
    average_deposit: float,
    operators_satisfaction: float,
    created_at: int,
    updated_at: int
  ):
    if not entity_id:
      raise EntityError("entity_id")
    if not self.validate_uuid(entity_id):
      raise EntityError("entity_id")
    if not registers:
      raise EntityError("registers")
    if not ftds:
      raise EntityError("ftds")
    if not rev_share:
      raise EntityError("rev_share")
    if not costs_per_acquisition:
      raise EntityError("costs_per_acquisition")
    if not shipping_volume:
      raise EntityError("shipping_volume")
    if not base_quality:
      raise EntityError("base_quality")
    if not commission_total_paid:
      raise EntityError("commission_total_paid")
    if not average_deposit:
      raise EntityError("average_deposit")
    if not operators_satisfaction:
      raise EntityError("operators_satisfaction")
    if not self.validate_timestamp(created_at):
      raise EntityError("created_at")
    if not self.validate_timestamp(updated_at):
      raise EntityError("updated_at")
    return True
  
  def to_dict(self) -> dict:
    return {
      "entity_id": self.entity_id,
      "registers": self.registers,
      "ftds": self.ftds,
      "rev_share": self.rev_share,
      "costs_per_acquisition": self.costs_per_acquisition,
      "shipping_volume": self.shipping_volume,
      "base_quality": self.base_quality,
      "commission_total_paid": self.commission_total_paid,
      "average_deposit": self.average_deposit,
      "operators_satisfaction": self.operators_satisfaction
    }
    
  @classmethod
  def from_dict(cls, data: dict) -> 'Entity':
    return cls(
      entity_id=data.get("entity_id"),
      registers=data.get("registers"),
      ftds=data.get("ftds"),
      rev_share=data.get("rev_share"),
      costs_per_acquisition=data.get("costs_per_acquisition"),
      shipping_volume=data.get("shipping_volume"),
      base_quality=data.get("base_quality"),
      commission_total_paid=data.get("commission_total_paid"),
      average_deposit=data.get("average_deposit"),
      operators_satisfaction=data.get("operators_satisfaction")
    )
  
  
  
  