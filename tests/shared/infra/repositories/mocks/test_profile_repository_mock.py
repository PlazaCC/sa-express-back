from src.shared.domain.entities.profile import Profile
from src.shared.domain.enums.profile_status_enum import PROFILE_STATUS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.mocks.profile_repository_mock import ProfileRepositoryMock


class Test_ProfileRepositoryMock:
  
  def test_create_profile(self):
    repo = ProfileRepositoryMock()
    
    profile = Profile(
      user_id="00000000-0000-0000-0000-000000000002",
      entity_id="00000000-0000-0000-0000-000000000002",
      game_data_id="00000000-0000-0000-0000-000000000002",
      affiliations=[
          "00000000-0000-0000-0000-000000000002",
      ],
      wallet_id="00000000-0000-0000-0000-000000000002",
      role=ROLE.ADMIN,
      created_at=1610000000,
      updated_at=1610000000,
    )
    
    repo.create_profile(profile)
    
    assert len(repo.profiles) == 3
    assert repo.profiles[-1] == profile
    
  def test_get_profile_by_id(self):
    repo = ProfileRepositoryMock()
    
    profile = repo.get_profile_by_id("00000000-0000-0000-0000-000000000000")
    
    assert profile.user_id == "00000000-0000-0000-0000-000000000000"
    assert profile.entity_id == "00000000-0000-0000-0000-000000000000"
    assert profile.game_data_id == "00000000-0000-0000-0000-000000000000"
    assert profile.affiliations == ["00000000-0000-0000-0000-000000000000"]
    assert profile.wallet_id == "00000000-0000-0000-0000-000000000000"
    assert profile.role == ROLE.ADMIN
    assert profile.created_at == 1610000000
    assert profile.updated_at == 1610000000
    
  def test_deactivate_profile(self):
    repo = ProfileRepositoryMock()
    
    profile = repo.deactivate_profile("00000000-0000-0000-0000-000000000000")
    
    assert profile.user_id == "00000000-0000-0000-0000-000000000000"
    assert profile.entity_id == "00000000-0000-0000-0000-000000000000"
    assert profile.game_data_id == "00000000-0000-0000-0000-000000000000"
    assert profile.affiliations == ["00000000-0000-0000-0000-000000000000"]
    assert profile.wallet_id == "00000000-0000-0000-0000-000000000000"
    assert profile.role == ROLE.ADMIN
    assert profile.created_at == 1610000000
    assert profile.updated_at == 1610000000
    assert profile.status == PROFILE_STATUS.INACTIVE