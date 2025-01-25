from typing import List
from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.repositories.affiliation_repository_interface import IAffiliationRepository


class AffiliationRepositoryMock(IAffiliationRepository):
  affiliations: List[Affiliation]
  
  def __init__(self):
    self.affiliations = [
      Affiliation(
        affiliation_id="00000000-0000-0000-0000-000000000000",
        deal_id="00000000-0000-0000-0000-000000000000",
        user_id="00000000-0000-0000-0000-000000000000",
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
        cost_per_acquisition=3,
        ftd=3,
        invoiced_amount=3,
        operators_satisfaction=3,
        registers=3,
        rev_share=3,
        shipping_volume=3,
      )
    ]
    
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