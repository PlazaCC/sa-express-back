from typing import List
from src.shared.domain.entities.profile import Profile
from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.enums.profile_status_enum import PROFILE_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository


class ProfileRepositoryMock(IProfileRepository):
    profiles: List[Profile]

    def __init__(self):
        self.profiles = [
            Profile(
                user_id="00000000-0000-0000-0000-000000000000",
                entity_id="00000000-0000-0000-0000-000000000000",
                game_data_id="00000000-0000-0000-0000-000000000000",
                affiliations=[
                    "00000000-0000-0000-0000-000000000000",
                ],
                wallet_id="00000000-0000-0000-0000-000000000000",
                role=ROLE.ADMIN,
                created_at=1610000000,
                updated_at=1610000000,
            ),
            Profile(
                user_id="00000000-0000-0000-0000-000000000001",
                entity_id="00000000-0000-0000-0000-000000000001",
                game_data_id="00000000-0000-0000-0000-000000000001",
                affiliations=[
                    "00000000-0000-0000-0000-000000000001",
                ],
                wallet_id="00000000-0000-0000-0000-000000000001",
                role=ROLE.ADMIN,
                created_at=1620000000,
                updated_at=1620000000,
            ),
        ]

    def get_profile_by_id(self, user_id: str) -> Profile:
        for profile in self.profiles:
            if profile.user_id == user_id:
                return profile
        return None
    
    def create_profile(self, profile):
        self.profiles.append(profile)
        return profile
    
    def deactivate_profile(self, user_id):
        for profile in self.profiles:
            if profile.user_id == user_id:
                profile.status = PROFILE_STATUS.INACTIVE
                return profile
        return None
