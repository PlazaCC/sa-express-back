from src.shared.domain.entities.affiliation import Affiliation
from src.shared.infra.repositories.mocks.affiliation_repository_mock import AffiliationRepositoryMock


class Test_AffiliationRepositoryMock:
  
  def test_create_affiliation(self):
    repo = AffiliationRepositoryMock()
    
    affiliation = Affiliation(
      affiliation_id="00000000-0000-0000-0000-000000000003",
      deal_id="00000000-0000-0000-0000-000000000003",
      user_id="00000000-0000-0000-0000-000000000003",
      amount_to_pay=1,
      baseline=1,
      commission=1,
      cost_per_acquisition=1,
      ftd=1,
      invoiced_amount=1,
      operators_satisfaction=1,
      base_quality=1,
      registers=1,
      rev_share=1,
      shipping_volume=1,
    )
    
    repo.create_affiliation(affiliation)
    
    assert len(repo.affiliations) == 4
    assert repo.affiliations[-1] == affiliation
    
  def test_get_affiliation_by_id(self):
    repo = AffiliationRepositoryMock()
    
    affiliation = repo.get_affiliation_by_id("00000000-0000-0000-0000-000000000000")
    
    assert affiliation.affiliation_id == "00000000-0000-0000-0000-000000000000"
    assert affiliation.deal_id == "00000000-0000-0000-0000-000000000000"
    assert affiliation.user_id == "00000000-0000-0000-0000-000000000000"
    assert affiliation.amount_to_pay == 1
    assert affiliation.baseline == 1
    assert affiliation.commission == 1
    assert affiliation.cost_per_acquisition == 1
    assert affiliation.ftd == 1
    assert affiliation.invoiced_amount == 1
    assert affiliation.operators_satisfaction == 1
    assert affiliation.registers == 1
    assert affiliation.rev_share == 1
    assert affiliation.shipping_volume == 1
    
  def test_get_all_my_affiliations(self):
    repo = AffiliationRepositoryMock()
    
    affiliations = repo.get_all_my_affiliations("00000000-0000-0000-0000-000000000000")
    
    assert len(affiliations) == 1
    assert affiliations[0].affiliation_id == "00000000-0000-0000-0000-000000000000"
    assert affiliations[0].deal_id == "00000000-0000-0000-0000-000000000000"
    assert affiliations[0].user_id == "00000000-0000-0000-0000-000000000000"
    assert affiliations[0].amount_to_pay == 1
    assert affiliations[0].baseline == 1
    assert affiliations[0].commission == 1
    assert affiliations[0].cost_per_acquisition == 1
    assert affiliations[0].ftd == 1
    assert affiliations[0].invoiced_amount == 1
    assert affiliations[0].operators_satisfaction == 1
    assert affiliations[0].registers == 1
    assert affiliations[0].rev_share == 1
    assert affiliations[0].shipping_volume == 1
    
  def test_get_all_my_affiliations_no_affiliations(self):
    repo = AffiliationRepositoryMock()
    
    affiliations = repo.get_all_my_affiliations("00000000-0000-0000-0000-000000000003")
    
    assert len(affiliations) == 0
    