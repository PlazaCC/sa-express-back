from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS
from src.shared.domain.enums.proposal_type_enum import PROPOSAL_TYPE

class Proposal(BaseModel, ABC):    
    proposal_id: str = Field(..., min_length=36, max_length=36, description="String com exatamente 36 caracteres")
    user_id: str = Field(..., min_length=36, max_length=36, description="ID do usuário que enviou a proposta")
    proposal_type: PROPOSAL_TYPE = Field(..., description="Tipo da proposta")
    status: PROPOSAL_STATUS = Field(..., description="Status da proposta")
    created_at: int = Field(..., gt=0, description="Timestamp de criação (deve ser um número positivo)")
    updated_at: int = Field(..., gt=0, description="Timestamp de atualização (deve ser um número positivo)")

    @field_validator("proposal_id", "proposer_id", "user_id")
    def validar_uuid(cls, value: str) -> str:
        if len(value) != 36:
            raise ValueError(f"O campo '{cls.__name__}' deve conter exatamente 36 caracteres.")
        return value
    
    @property
    @abstractmethod
    def proposal_type(self) -> PROPOSAL_TYPE:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "proposer_id": self.proposer_id,
            "receiver_id": self.receiver_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
class DealProposal(Proposal):    
    deal_id: str = Field(..., min_length=36, max_length=36, description="ID do negócio relacionado à proposta")
    entity_id: str = Field(..., min_length=36, max_length=36, description="ID da entidade relacionada à proposta")
    
    @field_validator("deal_id", "entity_id")
    def validar_uuid(cls, value: str) -> str:
        if len(value) != 36:
            raise ValueError(f"O campo '{cls.__name__}' deve conter exatamente 36 caracteres.")
        return value
    
    @property
    def proposal_type(self) -> PROPOSAL_TYPE:
        return PROPOSAL_TYPE.DEAL

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "deal_id": self.deal_id
        })
        return data