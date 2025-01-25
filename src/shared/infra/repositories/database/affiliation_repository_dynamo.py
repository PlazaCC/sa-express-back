from typing import List
from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.repositories.affiliation_repository_interface import IAffiliationRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo_datasource import DynamoDatasource


class AffiliationRepositoryDynamo(IAffiliationRepository):
  def __init__(self, dynamo: DynamoDatasource):
    self.dynamo = dynamo
  
  @staticmethod
  def affiliation_partition_key_format(user_id: str) -> str:
    return f'PROFILE#{user_id}'
  
  @staticmethod
  def affiliation_sort_key_format(deal_id) -> str:
    return f'AFFILIATION#{deal_id}'
  
  
  def get_affiliation_by_id(self, user_id) -> Affiliation:
    try:
      affiliation = self.dynamo.get_item(partition_key=self.affiliation_partition_key_format(user_id))
      
      if "Item" not in affiliation:
        return None
      
      return Affiliation.from_dict(affiliation['Item'])
    except Exception as e:
      raise e
    
  def create_affiliation(self, affiliation) -> Affiliation:
    try:
      self.dynamo.put_item(
        item=affiliation.to_dict(),
        partition_key=self.affiliation_partition_key_format(affiliation.user_id),
        sort_key=self.affiliation_sort_key_format(affiliation.deal_id)
      )
      return affiliation
    except Exception as e:
      raise e
    
  def get_all_my_affiliations(self, user_id) -> List[Affiliation]:
    try:
      affiliations = self.dynamo.query(partition_key=self.affiliation_partition_key_format(user_id))
      
      if "Items" not in affiliations:
        return []
      
      return [Affiliation.from_dict(affiliation) for affiliation in affiliations['Items']]
    except Exception as e:
      raise e
  
  
    
  