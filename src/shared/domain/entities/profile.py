from typing import List

from src.shared.domain.entities.affiliation import Affiliation
from src.shared.helpers.errors.errors import EntityError


class Profile:
  user_id: str
  bet_data_id: str
  game_data_id: str
  affiliations: List[Affiliation]
  wallet_id: str
  # tools needed new entity?
  # subscriptions needed new entity?
  
  def __init__(self, user_id: str, bet_data_id: str, game_data_id: str, affiliations: List[Affiliation], wallet_id: str):
    
    self.validator(user_id, bet_data_id, game_data_id, affiliations, wallet_id)

    self.user_id = user_id
    self.bet_data_id = bet_data_id
    self.game_data_id = game_data_id
    self.affiliations = affiliations
    self.wallet_id = wallet_id
    
  def validator(
    self,
    user_id: str,
    bet_data_id: str,
    game_data_id: str,
    affiliations: List[Affiliation],
    wallet_id: str
  ):
    if not user_id:
      raise EntityError("User ID is required")
    if not bet_data_id:
      raise EntityError("Bet Data ID is required")
    if not game_data_id:
      raise EntityError("Game Data ID is required")
    if not affiliations:
      raise EntityError("Affiliations are required")
    if not wallet_id:
      raise EntityError("Wallet ID is required")
    return True
  