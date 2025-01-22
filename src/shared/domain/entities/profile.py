from pydantic import Field, field_validator
from typing import List

from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.enums.profile_status_enum import PROFILE_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import EntityError


class Profile:
  user_id: str = Field(..., description="String with 32 characters")
  bet_data_id: str = Field(..., description="String with 32 characters")
  game_data_id: str = Field(..., description="String with 32 characters")
  affiliations: List[Affiliation]
  wallet_id: str = Field(..., description="String with 32 characters")
  status: PROFILE_STATUS
  role: ROLE
  created_at: int = Field(..., description="Timestamp in seconds")
  updated_at: int = Field(..., description="Timestamp in seconds")
  # tools needed new entity?
  # subscriptions needed new entity?
  
  def __init__(self, user_id: str, bet_data_id: str, game_data_id: str, affiliations: List[Affiliation], wallet_id: str, role: ROLE, created_at: int, updated_at: int, status: PROFILE_STATUS = PROFILE_STATUS.ACTIVE):
    
    self.validator(user_id, bet_data_id, game_data_id, affiliations, wallet_id, role)

    self.user_id = user_id
    self.bet_data_id = bet_data_id
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
    bet_data_id: str,
    game_data_id: str,
    affiliations: List[Affiliation],
    wallet_id: str,
    role: ROLE,
  ):
    if not user_id:
      raise EntityError("user_id")
    if not bet_data_id:
      raise EntityError("bet_data_id")
    if not game_data_id:
      raise EntityError("game_data_id")
    if not affiliations:
      raise EntityError("affiliations")
    if not wallet_id:
      raise EntityError("wallet_id")
    if not self.validate_uuid(user_id):
      raise EntityError("user_id")
    if not self.validate_uuid(bet_data_id):
      raise EntityError("bet_data_id")
    if not self.validate_uuid(game_data_id):
      raise EntityError("game_data_id")
    if not self.validate_uuid(wallet_id):
      raise EntityError("wallet_id")
    if not isinstance(affiliations, list):
      raise EntityError("affiliations")
    for affiliation in affiliations:
      if not isinstance(affiliation, Affiliation):
        raise EntityError("affiliation")
    if not isinstance(role, ROLE):
      raise EntityError("role")
    return True
  
  @field_validator('user_id', 'bet_id', 'game_id', 'wallet_id')
  @staticmethod
  def validate_uuid(value: str) -> str:
      if not isinstance(value, str):
          raise EntityError
      if len(value) != 36:
          raise ValueError("deal_id and bet_id must have exactly 36 characters")
      return value
  
  def to_dict(self):
        return {
          "user": {
            "user_id": self.user_id,
            "bet_data_id": self.bet_data_id,
            "game_data_id": self.game_data_id,
            "affiliations": [affiliation.to_dict() for affiliation in self.affiliations],
            "wallet_id": self.wallet_id,
            "status": self.status.value,
            "role": self.role.value,
          }
        }
  