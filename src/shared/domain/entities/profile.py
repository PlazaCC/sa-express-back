from pydantic import BaseModel, Field, field_validator
from typing import Any, List

from src.shared.domain.enums.profile_status_enum import PROFILE_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import EntityError


class Profile(BaseModel):
  user_id: str = Field(..., description="String with 32 characters")
  entity_id: str = Field(..., description="String with 32 characters")
  game_data_id: str = Field(..., description="String with 32 characters")
  affiliations: List[str]
  wallet_id: str = Field(..., description="String with 32 characters")
  status: PROFILE_STATUS = Field(default=PROFILE_STATUS.ACTIVE)
  role: ROLE
  created_at: int = Field(..., description="Timestamp in seconds")
  updated_at: int = Field(..., description="Timestamp in seconds")
  # tools needed new entity?
  # subscriptions needed new entity?
  
  @field_validator('user_id', 'entity_id', 'game_data_id', 'wallet_id')
  @staticmethod
  def validate_uuid(value: str) -> str:
      if not isinstance(value, str):
          raise ValueError("uuids precisam ser strings")
      if len(value) != 36:
          raise ValueError("uuids devem ter exatamente 36 caracteres")
      return value
    
  @field_validator('created_at', 'updated_at')
  @staticmethod
  def validate_timestamp(value: Any) -> int:
      if not isinstance(value, int):
          raise ValueError("created_at e updated_at devem ser inteiros representando timestamps")
      if value < 0:
          raise ValueError("Timestamps devem ser inteiros positivos")
      return value
  
  def to_dict(self):
    return {
      "user_id": self.user_id,
      "entity_id": self.entity_id,
      "game_data_id": self.game_data_id,
      "affiliations": self.affiliations,
      "wallet_id": self.wallet_id,
      "status": self.status.value,
      "role": self.role.value,
    }
    
  @classmethod
  def from_dict(cls, data: dict) -> 'Profile':
    return cls(
      user_id=data.get("user_id"),
      entity_id=data.get("entity_id"),
      game_data_id=data.get("game_data_id"),
      affiliations=data.get("affiliations"),
      wallet_id=data.get("wallet_id"),
      status=PROFILE_STATUS[data.get("status")],
      role=ROLE[data.get("role")],
      created_at=data.get("created_at"),
      updated_at=data.get("updated_at"),
    )
  