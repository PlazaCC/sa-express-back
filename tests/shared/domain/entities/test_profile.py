import pytest
from src.shared.domain.entities.profile import Profile
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.errors import EntityError


class Test_Profile:
  
  def test_profile(self):
    profile = Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", game_data_id="00000000-0000-0000-0000-000000000000", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at=1, updated_at=1)
    
    assert profile.user_id == "00000000-0000-0000-0000-000000000000"
    assert profile.entity_id == "00000000-0000-0000-0000-000000000000"
    assert profile.game_data_id == "00000000-0000-0000-0000-000000000000"
    assert profile.affiliations == ["00000000-0000-0000-0000-000000000000"]
    assert profile.wallet_id == "00000000-0000-0000-0000-000000000000"
    assert profile.role == ROLE.ADMIN
    assert profile.created_at == 1
    assert profile.updated_at == 1
    
  def test_user_id_not_string(self):
    with pytest.raises(ValueError):
      Profile(user_id=1, entity_id="00000000-0000-0000-0000-000000000000", game_data_id="00000000-0000-0000-0000-000000000000", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at=1, updated_at=1)
      
  def test_user_id_not_36_characters(self):
    with pytest.raises(ValueError):
      Profile(user_id="1", entity_id="00000000-0000-0000-0000-000000000000", game_data_id="00000000-0000-0000-0000-000000000000", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at=1, updated_at=1)
      
  def test_entity_id_not_string(self):
    with pytest.raises(ValueError):
      Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id=1, game_data_id="00000000-0000-0000-0000-000000000000", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at=1, updated_at=1)
      
  def test_entity_id_not_36_characters(self):
    with pytest.raises(ValueError):
      Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id="1", game_data_id="00000000-0000-0000-0000-000000000000", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at=1, updated_at=1)
      
  def test_game_data_id_not_string(self):
    with pytest.raises(ValueError):
      Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", game_data_id=1, affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at=1, updated_at=1)
      
  def test_game_data_id_not_36_characters(self):
    with pytest.raises(ValueError):
      Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", game_data_id="1", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at=1, updated_at=1)
      
  def test_affiliations_not_list(self):
    with pytest.raises(ValueError):
      Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", game_data_id="00000000-0000-0000-0000-000000000000", affiliations="00000000-0000-0000-0000-000000000000", wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at=1, updated_at=1)
      
  def test_wallet_id_not_string(self):
    with pytest.raises(ValueError):
      Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", game_data_id="00000000-0000-0000-0000-000000000000", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id=1, role=ROLE.ADMIN, created_at=1, updated_at=1)
      
  def test_wallet_id_not_36_characters(self):
    with pytest.raises(ValueError):
      Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", game_data_id="00000000-0000-0000-0000-000000000000", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="1", role=ROLE.ADMIN, created_at=1, updated_at=1)
      
  def test_created_at_not_integer(self):
    with pytest.raises(ValueError):
      Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", game_data_id="00000000-0000-0000-0000-000000000000", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at="not_an_int", updated_at=1)
      
  def test_updated_at_not_integer(self):
    with pytest.raises(ValueError):
      Profile(user_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", game_data_id="00000000-0000-0000-0000-000000000000", affiliations=["00000000-0000-0000-0000-000000000000"], wallet_id="00000000-0000-0000-0000-000000000000", role=ROLE.ADMIN, created_at=1, updated_at="not_an_int")