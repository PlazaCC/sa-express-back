from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.influencer import Influencer


class IInfluencerRepository(ABC):
  @abstractmethod
  def get_influencer(self, user_id: str) -> Influencer:
    pass

  @abstractmethod
  def get_all_influencers(self) -> dict : # type: ignore
    pass

  @abstractmethod
  def create_influencer(self, influencer: Influencer) -> None:
    pass