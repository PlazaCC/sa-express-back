from typing import List

from src.shared.domain.enums.role_enum import ROLE

class UserApiGatewayDTO:
    user_id: str
    name: str
    email: str
    role: ROLE

    def __init__(self, user_id: str, name: str, email: str, role: ROLE):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
    
    @staticmethod
    def from_api_gateway(user_data: dict) -> 'UserApiGatewayDTO':
        return UserApiGatewayDTO(
            user_id=user_data['sub'],
            name=user_data['name'],
            email=user_data['email'],
            role=ROLE[user_data['custom:role']]
        )
    
    def __eq__(self, other):
        return self.user_id == other.user_id and self.email == other.email and self.role == other.role and self.name == other.name