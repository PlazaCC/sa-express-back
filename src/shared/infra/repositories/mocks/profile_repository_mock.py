from typing import List
from src.shared.domain.entities.profile import Profile
from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository


class ProfileRepositoryMock(IProfileRepository):
    profiles: List[Profile]

    def __init__(self):
        self.profiles = [
            Profile(
                user_id="00000000-0000-0000-0000-000000000000",
                bet_data_id="bet-0000",
                game_data_id="game-0000",
                affiliations=[
                    Affiliation(
                        affiliation_id="aff-0000",
                        invoiced_amount=1000.0,
                        amount_to_pay=500.0,
                        commission=10.0,
                        baseline=1.0,
                        cost_per_acquisition=2,
                        rev_share=0.1,
                        registers=10,
                        ftd=5,
                        shipping_volume=20.0,
                        base_quality=90.0,
                        operators_satisfaction=95.0
                    )
                ],
                wallet_id="wallet-0000"
            ),
            Profile(
                user_id="00000000-0000-0000-0000-000000000001",
                bet_data_id="bet-0001",
                game_data_id="game-0001",
                affiliations=[
                    Affiliation(
                        affiliation_id="aff-0001",
                        invoiced_amount=2000.0,
                        amount_to_pay=1000.0,
                        commission=15.0,
                        baseline=2.0,
                        cost_per_acquisition=3,
                        rev_share=0.15,
                        registers=20,
                        ftd=10,
                        shipping_volume=30.0,
                        base_quality=85.0,
                        operators_satisfaction=90.0
                    )
                ],
                wallet_id="wallet-0001"
            ),
        ]

    def get_profile_by_id(self, user_id: str) -> Profile:
        for profile in self.profiles:
            if profile.user_id == user_id:
                return profile
        return None
