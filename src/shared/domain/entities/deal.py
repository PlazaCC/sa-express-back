from pydantic import BaseModel, Field, field_validator
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from typing import Any


class Deal(BaseModel):
    deal_id: str = Field(..., description="String with 32 characters")
    bet_id: str = Field(..., description="String with 32 characters")
    baseline: float
    cpa: float
    rev_share: float
    conditions: str
    deal_status: DEAL_STATUS
    created_at: int = Field(..., description="Timestamp in seconds")
    updated_at: int = Field(..., description="Timestamp in seconds")

    @field_validator('deal_id', 'bet_id')
    @staticmethod
    def validate_uuid(value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("deal_id and bet_id must be strings")
        if len(value) != 36:
            raise ValueError("deal_id and bet_id must have exactly 36 characters")
        return value

    @field_validator('created_at', 'updated_at')
    @staticmethod
    def validate_timestamp(value: Any) -> int:
        if not isinstance(value, int):
            raise ValueError("created_at and updated_at must be integers representing timestamps")
        if value < 0:
            raise ValueError("Timestamps must be positive integers")
        return value

    def to_dict(self):
        return {
            "deal_id": self.deal_id,
            "bet_id": self.bet_id,
            "baseline": self.baseline,
            "cpa": self.cpa,
            "rev_share": self.rev_share,
            "conditions": self.conditions,
            "deal_status": self.deal_status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Deal':
        return cls(
            deal_id=data.get("deal_id"),
            bet_id=data.get("bet_id"),
            baseline=data.get("baseline"),
            cpa=data.get("cpa"),
            rev_share=data.get("rev_share"),
            conditions=data.get("conditions"),
            deal_status=DEAL_STATUS[data.get("deal_status")],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
