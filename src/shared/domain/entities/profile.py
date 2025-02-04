from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Any, Dict, Optional
from src.shared.domain.enums.role_enum import ROLE

class Profile(BaseModel):  # METADATA ONLY
    user_id: str = Field(..., description="String with 32 characters")
    role: ROLE = Field(..., description="Role of the user")
    entity_id: Optional[str] = Field(None, description="String with 32 characters")
    status: bool = Field(default=True, description="Status of the profile")
    created_at: int = Field(..., description="Timestamp in seconds", gt=0)
    updated_at: int = Field(..., description="Timestamp in seconds", gt=0)

    @field_validator('user_id')
    @staticmethod
    def validate_user_id(value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("user_id deve ser uma string")
        if len(value) != 32:
            raise ValueError("user_id deve ter exatamente 32 caracteres")
        return value

    @field_validator('entity_id')
    @classmethod
    def validate_entity_id(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        role = values.get("role")
        
        if role == ROLE.OPERADOR:
            if not isinstance(v, str) or len(v) != 32:
                raise ValueError("entity_id deve ser uma string de 32 caracteres quando o cargo é ROLE.OPERADOR")
        else:
            if v not in (None, ''):
                raise ValueError("Apenas usuários com cargo ROLE.OPERADOR podem ter entity_id preenchido")
        return v

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "entity_id": self.entity_id,
            "status": self.status,
            "role": self.role.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Profile':
        return cls(
            user_id=data.get("user_id"),
            entity_id=data.get("entity_id"),
            status=data.get("status"),
            role=ROLE[data.get("role")],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
