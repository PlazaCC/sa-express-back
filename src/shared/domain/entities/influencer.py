from typing import List
from pydantic import BaseModel, Field, field_validator

class Followers(BaseModel):
  instagram: int = Field(..., description="Instagram followers count")
  tiktok: int = Field(..., description="TikTok followers count")


class Influencer(BaseModel):
  user_id: str = Field(..., description="String with 32 characters")
  ftd: int = Field(..., description="First time deposits")
  cpa: float = Field(..., description="Cost per acquisition")
  total_commission: float = Field(..., description="Total commission")
  name: str = Field(..., description="Influencer name")
  followers: Followers = Field(..., description="Followers count")
  story_count: int = Field(..., description="Number of stories")
  price: float = Field(..., description="Price of the influencer")
  views: int = Field(..., description="Number of views")
  story_gallery: List[str] = Field(..., description="List of stories videos urls or images urls")
  
  
  @field_validator('user_id')
  @staticmethod
  def validate_user_id(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("user_id deve ser uma string")
    if len(value) != 32:
        raise ValueError("user_id deve ter exatamente 32 caracteres")
    return value
  
  def to_dict(self) -> dict:
    return {
        "user_id": self.user_id,
        "ftd": self.ftds,
        "cpa": self.cpa,
        "total_commission": self.total_commission,
        "name": self.name,
        "followers": self.followers,
        "story_count": self.story_count,
        "price": self.price
    }
    
  @classmethod
  def from_dict(cls, data: dict) -> 'Influencer':
    return cls(
        user_id=data.get("user_id"),
        ftd=data.get("ftd"),
        cpa=data.get("cpa"),
        total_commission=data.get("total_commission"),
        name=data.get("name"),
        followers=Followers(**data.get("followers")),
        story_count=data.get("story_count"),
        price=data.get("price")
    )
  
  
  
  
  