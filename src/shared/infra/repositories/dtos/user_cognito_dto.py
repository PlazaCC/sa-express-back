from enum import Enum
from typing import List, Optional
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS


class UserCognitoDTO:
    user_id: int
    name: str
    email: str
    phone: str
    role: ROLE
    user_status: USER_STATUS
    created_at: str
    updated_at: str
    email_verified: bool
    enabled: bool

    def __init__(self,
                user_id: int,
                name: str,
                email: str,
                phone: str,
                role: ROLE,
                user_status: USER_STATUS,
                created_at: str,
                updated_at: str,
                email_verified: bool,
                enabled: bool,):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.user_status = user_status
        self.created_at = created_at
        self.updated_at = updated_at
        self.email_verified = email_verified
        self.enabled = enabled


    @staticmethod
    def from_entity(user: User):
        return UserCognitoDTO(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            role=user.role,
            phone=user.phone,
            user_status=user.user_status,
            created_at=user.created_at,
            updated_at=user.updated_at,
            email_verified=user.email_verified,
            enabled=user.enabled
        )

    TO_COGNITO_DICT = {
        "email": "email",
        "name": "name",
        "role": "custom:general_role",
        "phone": "phone",
    }

    FROM_COGNITO_DICT = {value: key for key, value in TO_COGNITO_DICT.items()}
    FROM_COGNITO_DICT["sub"] = "user_id"

    def to_cognito_attributes(self) -> List[dict]:
        user_attributes = []
        for att, name in self.TO_COGNITO_DICT.items():
            value = getattr(self, att)
            if isinstance(value, Enum):  # Verifica se é um enum
                value = value.value  # Obtém o valor do enum
            user_attributes.append(self.parse_attribute(value=value, name=name))
        
        user_attributes = [att for att in user_attributes if att["Value"] != str(None)]

        return user_attributes
    
    @staticmethod
    def from_cognito(data: dict) -> "UserCognitoDTO":
        user_data = next((value for key, value in data.items() if "Attribute" in key), None)
        user_data = {UserCognitoDTO.FROM_COGNITO_DICT[att["Name"]]: att["Value"] for att in user_data if att["Name"] in UserCognitoDTO.FROM_COGNITO_DICT}
        # user_data["created_at"] = data.get("UserCreateDate")
        # user_data["updated_at"] = data.get("UserLastModifiedDate")
        user_data["enabled"] = data.get("Enabled")
        user_data["status"] = data.get("UserStatus")

        return UserCognitoDTO(
            user_id=str(user_data["user_id"]),
            email=str(user_data["email"]),
            name=str(user_data["name"]),
            role = ROLE[user_data["role"]],
            enabled=bool(user_data["enabled"]),
            user_status=USER_STATUS[user_data["status"]],
            created_at=str(user_data["created_at"]),
            updated_at=str(user_data["updated_at"]),
            email_verified=bool(user_data["email_verified"]),
            phone=str(user_data["phone"])
        )

    def to_entity(self) -> User:
        return User(
            user_id=self.user_id,
            email=self.email,
            name=self.name,
            role=self.role,
            phone=self.phone,
            user_status=self.user_status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            email_verified=self.email_verified,
            enabled=self.enabled
        )
    
    @staticmethod
    def parse_attribute(name, value) -> dict:
        return {'Name': name, 'Value': str(value)}


