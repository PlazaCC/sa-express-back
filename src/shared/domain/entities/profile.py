from pydantic import Field, field_validator
from typing import Any, List

from src.shared.domain.enums.profile_status_enum import PROFILE_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import EntityError


class Profile:
  user_id: str = Field(..., description="String with 32 characters")
  entity_id: str = Field(..., description="String with 32 characters")
  game_data_id: str = Field(..., description="String with 32 characters")
  affiliations: List[str]
  wallet_id: str = Field(..., description="String with 32 characters")
  status: PROFILE_STATUS
  role: ROLE
  created_at: int = Field(..., description="Timestamp in seconds")
  updated_at: int = Field(..., description="Timestamp in seconds")
  # tools needed new entity?
  # subscriptions needed new entity?
  
  def __init__(self, user_id: str, entity_id: str, game_data_id: str, affiliations: List[str], wallet_id: str, role: ROLE, created_at: int, updated_at: int, status: PROFILE_STATUS = PROFILE_STATUS.ACTIVE):
    
    self.validator(user_id, entity_id, game_data_id, affiliations, wallet_id, role, created_at, updated_at)

    self.user_id = user_id
    self.entity_id = entity_id
    self.game_data_id = game_data_id
    self.affiliations = affiliations
    self.wallet_id = wallet_id
    self.status = status
    self.role = role
    self.created_at = created_at
    self.updated_at = updated_at
    
  def validator(
    self,
    user_id: str,
    entity_id: str,
    game_data_id: str,
    affiliations: List[str],
    wallet_id: str,
    role: ROLE,
    created_at: int,
    updated_at: int,
  ):
    if not user_id:
      raise EntityError("user_id")
    if not entity_id:
      raise EntityError("entity_id")
    if not game_data_id:
      raise EntityError("game_data_id")
    if not affiliations:
      raise EntityError("affiliations")
    if not wallet_id:
      raise EntityError("wallet_id")
    for afiliation in affiliations:
      if not self.validate_uuid(afiliation):
        raise EntityError("affiliation")
    if not self.validate_uuid(user_id):
      raise EntityError("user_id")
    if not self.validate_uuid(entity_id):
      raise EntityError("entity_id")
    if not self.validate_uuid(game_data_id):
      raise EntityError("game_data_id")
    if not self.validate_uuid(wallet_id):
      raise EntityError("wallet_id")
    if not isinstance(affiliations, list):
      raise EntityError("affiliations")
    if not isinstance(role, ROLE):
      raise EntityError("role")
    if not self.validate_timestamp(created_at):
      raise EntityError("created_at")
    if not self.validate_timestamp(updated_at):
      raise EntityError("updated_at")
    return True
  
  @field_validator('user_id', 'entity_id', 'game_id', 'wallet_id')
  @staticmethod
  def validate_uuid(value: str) -> str:
      if not isinstance(value, str):
          raise EntityError("uuids precisam ser strings")
      if len(value) != 36:
          raise EntityError("uuids devem ter exatamente 36 caracteres")
      return value
    
  @field_validator('created_at', 'updated_at')
  @staticmethod
  def validate_timestamp(value: Any) -> int:
      if not isinstance(value, int):
          raise EntityError("created_at e updated_at devem ser inteiros representando timestamps")
      if value < 0:
          raise EntityError("Timestamps devem ser inteiros positivos")
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
  