from pydantic import BaseModel

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS


class User(BaseModel): # Cognito
  user_id: int
  name: str
  email: int
  role: ROLE
  user_status: USER_STATUS
  created_at: str
  updated_at: str
  email_verified: bool
  enabled: bool

  @staticmethod
  def from_dict_static(data):
    return User(
      user_id=data['user_id'],
      name=data['name'],
      email=data['email'],
      role=ROLE[data['role']],
      user_status=USER_STATUS[data['user_status']],
      created_at=data['created_at'],
      updated_at=data['updated_at'],
      email_verified=data['email_verified'],
      enabled=data['enabled']
    )
  
  def to_dict(self):
    return {
      "user_id": self.user_id,
      "name": self.name,
      "email": self.email,
      "role": self.role.value,
      "user_status": self.user_status.value,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
      "email_verified": self.email_verified,
      "enabled": self.enabled
    }
  
  def from_dict(self, data: dict) -> 'User':
    return User(
      user_id=data['user_id'],
      name=data['name'],
      email=data['email'],
      role=ROLE[data['role']],
      user_status=USER_STATUS[data['user_status']],
      created_at=data['created_at'],
      updated_at=data['updated_at'],
      email_verified=data['email_verified'],
      enabled=data['enabled']
    )