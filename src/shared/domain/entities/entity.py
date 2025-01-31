from typing import Any, Dict, List
from pydantic import BaseModel, Field, field_validator

class Banner(BaseModel):
    logo_url: str = Field(..., description="URL of the logo stored in S3")
    color: str = Field(..., description="Hexadecimal color code")

    def to_dict(self) -> dict:
        return {
            "logo_url": self.logo_url,
            "color": self.color
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Banner':
        return cls(
            logo_url=data.get("logo_url"),
            color=data.get("color")
        )

class Entity(BaseModel):  # METADATA
    entity_id: str = Field(..., description="String with 36 characters")
    name: str
    description: str
    banner: Banner
    created_at: int = Field(..., description="Timestamp in seconds", gt=0)
    updated_at: int = Field(..., description="Timestamp in seconds", gt=0)

    @field_validator('entity_id')
    @staticmethod
    def validate_uuid(value: str) -> str:
        if len(value) != 36:
            raise ValueError("entity_id must have exactly 36 characters")
        return value

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "description": self.description,
            "banner": self.banner.to_dict(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Entity':
        return cls(
            entity_id=data.get("entity_id"),
            name=data.get("name"),
            description=data.get("description"),
            banner=Banner.from_dict(data.get("banner")),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
