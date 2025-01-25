from typing import Any, List

from pydantic import BaseModel, Field, field_validator

from src.shared.helpers.errors.errors import EntityError


class Entity(BaseModel):
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
    
  @field_validator('entity_id')
  @staticmethod
  def validate_uuid(value: str) -> str:
      if not isinstance(value, str):
          raise ValueError("uuids must be strings")
      if len(value) != 36:
          raise ValueError("uuids must have exactly 36 characters")
      return value
    
  @field_validator('created_at', 'updated_at')
  @staticmethod
  def validate_timestamp(value: Any) -> int:
      if not isinstance(value, int):
          raise ValueError("created_at e updated_at devem ser inteiros representando timestamps")
      if value < 0:
          raise ValueError("Timestamps devem ser inteiros positivos")
      return value
  
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
  
  
  
  