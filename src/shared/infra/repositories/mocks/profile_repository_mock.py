from typing import List
from src.shared.domain.entities.profile import Profile
from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.enums.profile_status_enum import PROFILE_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository
from src.shared.domain.entities.affiliation import Affiliation


class ProfileRepositoryMock(IProfileRepository):
    profiles: List[Profile]
    affiliations: List[Affiliation]

    def __init__(self):
        self.profiles = [
            Profile(
                user_id="00000000-0000-0000-0000-000000000000",
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
        self.affiliations = [
            Affiliation(
                affiliation_id="00000000-0000-0000-0000-000000000000",
                deal_id="00000000-0000-0000-0000-000000000000",
                user_id="00000000-0000-0000-0000-000000000000",
                base_quality=1,
                amount_to_pay=1,
                baseline=1,
                commission=1,
                cost_per_acquisition=1,
                ftd=1,
                invoiced_amount=1,
                operators_satisfaction=1,
                registers=1,
                rev_share=1,
                shipping_volume=1,
            ),
            Affiliation(
                affiliation_id="00000000-0000-0000-0000-000000000001",
                deal_id="00000000-0000-0000-0000-000000000001",
                user_id="00000000-0000-0000-0000-000000000001",
                amount_to_pay=2,
                base_quality=2,
                baseline=2,
                commission=2,
                cost_per_acquisition=2,
                ftd=2,
                invoiced_amount=2,
                operators_satisfaction=2,
                registers=2,
                rev_share=2,
                shipping_volume=2,
            ),
            Affiliation(
                affiliation_id="00000000-0000-0000-0000-000000000002",
                deal_id="00000000-0000-0000-0000-000000000002",
                user_id="00000000-0000-0000-0000-000000000002",
                amount_to_pay=3,
                baseline=3,
                commission=3,
                base_quality=3,
                cost_per_acquisition=3,
                ftd=3,
                invoiced_amount=3,
                operators_satisfaction=3,
                registers=3,
                rev_share=3,
                shipping_volume=3,
            )
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
    
    def get_affiliation_by_id(self, user_id: str) -> Affiliation:
        for affiliation in self.affiliations:
            if affiliation.user_id == user_id:
                return affiliation
        return None
      
    def get_all_my_affiliations(self, user_id: str) -> List[Affiliation]:
        affiliations = []
        
        for affiliation in self.affiliations:
         if affiliation.user_id == user_id:
            affiliations.append(affiliation)
            
        return affiliations
    
    def create_affiliation(self, affiliation: Affiliation) -> Affiliation:
        self.affiliations.append(affiliation)
        return affiliation