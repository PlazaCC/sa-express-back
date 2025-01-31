from pydantic import BaseModel, Field, field_validator
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from typing import Any, List, Dict


class Deal(BaseModel):
    deal_id: str = Field(..., min_length=36, max_length=36, description="String com exatamente 36 caracteres")
    entity_id: str = Field(..., min_length=36, max_length=36, description="String com exatamente 36 caracteres")
    baseline: float = Field(..., ge=0, description="Valor base (deve ser maior ou igual a 0)")
    cpa: float = Field(..., ge=0, description="Custo por aquisição (deve ser maior ou igual a 0)")
    rev_share: float = Field(..., ge=0, le=1, description="Participação na receita (deve estar entre 0 e 1)")
    conditions: List[str] = Field(..., default=[], min_items=0, description="Lista de condições")
    deal_status: DEAL_STATUS = Field(default=DEAL_STATUS.ACTIVATED, description="Status do negócio")
    created_at: int = Field(..., gt=0, description="Timestamp de criação (deve ser um número positivo)")
    updated_at: int = Field(..., gt=0, description="Timestamp de atualização (deve ser um número positivo)")

    @field_validator("deal_id", "entity_id")
    def validar_uuid(cls, value: str) -> str:
        if len(value) != 36:
            raise ValueError(f"O campo '{cls.__name__}' deve conter exatamente 36 caracteres.")
        return value

    @field_validator("conditions", mode="before")
    def validar_conditions(cls, value: Any) -> List[str]:
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError("O campo 'conditions' deve ser uma lista de strings.")
        if len(value) == 0:
            raise ValueError("O campo 'conditions' deve ter pelo menos um item.")
        return value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "entity_id": self.entity_id,
            "baseline": self.baseline,
            "cpa": self.cpa,
            "rev_share": self.rev_share,
            "conditions": self.conditions,
            "deal_status": self.deal_status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Deal':
        return cls(
            deal_id=data.get("deal_id"),
            entity_id=data.get("entity_id"),
            baseline=data.get("baseline", 0.0),
            cpa=data.get("cpa", 0.0),
            rev_share=data.get("rev_share", 0.0),
            conditions=data.get("conditions") or [],
            deal_status=DEAL_STATUS[data["deal_status"]] if data.get("deal_status") in DEAL_STATUS.__members__ else DEAL_STATUS.ACTIVATED,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
