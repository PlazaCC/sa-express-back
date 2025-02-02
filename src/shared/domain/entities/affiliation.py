from typing import Any, Dict
from pydantic import BaseModel, Field, field_validator

class Affiliation(BaseModel):
    affiliation_id: str = Field(..., description="String with 32 characters")
    user_id: str = Field(..., description="String with 32 characters")
    deal_id: str = Field(..., description="String with 32 characters")
    entity_id: str = Field(..., description="String with 32 characters")
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
    created_at: int = Field(..., description="Timestamp in seconds", gt=0)
    updated_at: int = Field(..., description="Timestamp in seconds", gt=0)

    @field_validator('affiliation_id', 'user_id', 'deal_id', 'entity_id')
    @staticmethod
    def validate_id_length(value: str) -> str:
        if len(value) != 32:
            raise ValueError("Each ID must have exactly 32 characters")
        return value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "affiliation_id": self.affiliation_id,
            "user_id": self.user_id,
            "deal_id": self.deal_id,
            "entity_id": self.entity_id,
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
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Affiliation':
        return cls(
            affiliation_id=data.get("affiliation_id"),
            user_id=data.get("user_id"),
            deal_id=data.get("deal_id"),
            entity_id=data.get("entity_id"),
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
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
