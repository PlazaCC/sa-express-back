from typing import Optional

from pydantic import BaseModel, Field, field_validator
from src.shared.helpers.errors.errors import EntityError


class Affiliation(BaseModel):
    affiliation_id: str = Field(..., description="String with 32 characters"),
    user_id: str = Field(..., description="String with 32 characters"),
    deal_id: str = Field(..., description="String with 32 characters"),
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

    @field_validator('user_id', 'deal_id', 'affiliation_id')
    @staticmethod
    def validate_uuid(value: str) -> str:
        if not isinstance(value, str):
            raise EntityError
        if len(value) != 36:
            raise ValueError("uuids must have exactly 36 characters")
        return value

    def to_dict(self) -> dict:
      return {
        "affiliation_id": self.affiliation_id,
        "invoiced_amount": self.invoiced_amount,
        "amount_to_pay": self.amount_to_pay,
        "commission": self.commission,
        "baseline": self.baseline,
        "cost_per_acquisition": self.cost_per_acquisition,
        "rev_share": self.rev_share,
        "registers": self.registers,
        "ftd": self.ftd,
        "shipping_volume": self.shipping_volume,
        "base_quality": self.base_quality,
        "operators_satisfaction": self.operators_satisfaction,
      }

    @classmethod
    def from_dict(cls, data: dict) -> 'Affiliation':
      return cls(
        affiliation_id=data.get("affiliation_id"),
        invoiced_amount=data.get("invoiced_amount"),
        amount_to_pay=data.get("amount_to_pay"),
        commission=data.get("commission"),
        baseline=data.get("baseline"),
        cost_per_acquisition=data.get("cost_per_acquisition"),
        rev_share=data.get("rev_share"),
        registers=data.get("registers"),
        ftd=data.get("ftd"),
        shipping_volume=data.get("shipping_volume"),
        base_quality=data.get("base_quality"),
        operators_satisfaction=data.get("operators_satisfaction"),
      )
