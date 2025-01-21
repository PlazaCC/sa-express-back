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
                affiliations=[Affiliation(affiliation_id="aff-0000", name="Affiliation 1")],
                wallet_id="wallet-0000"
            ),
            Profile(
                user_id="00000000-0000-0000-0000-000000000001",
                bet_data_id="bet-0001",
                game_data_id="game-0001",
                affiliations=[Affiliation(affiliation_id="aff-0001", name="Affiliation 2")],
                wallet_id="wallet-0001"
            ),
        ]

    def get_profile_by_user_id(self, user_id: str) -> Profile:
        for profile in self.profiles:
            if profile.user_id == user_id:
                return profile
        return None
