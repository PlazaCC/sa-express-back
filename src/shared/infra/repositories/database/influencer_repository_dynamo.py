from src.shared.domain.entities.influencer import Influencer
from src.shared.domain.repositories.influencer_repository_interface import IInfluencerRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.key_formatters import influencer_gsi_primary_key, influencer_sort_key, profile_primary_key
from boto3.dynamodb.conditions import Key


class InfluencerRepositoryDynamo(IInfluencerRepository):
  
  def __init__(self, dynamo: DynamoDatasource):
    self.dynamo = dynamo
    
  def create_influencer(self, influencer: Influencer) -> Influencer:
    item = influencer.to_dict()
    item['PK'] = profile_primary_key(influencer.user_id)
    item['SK'] = influencer_sort_key()
    item['GSI#INFLUENCER'] = influencer_gsi_primary_key()
    
    self.dynamo.put_item(item=item)
    return influencer
  
  def get_influencer(self, user_id: str) -> Influencer:
    influencer = self.dynamo.get_item(
      partition_key=profile_primary_key(user_id),
      sort_key=influencer_sort_key()
    )
    
    if 'Item' not in influencer:
      return None
    
    return Influencer.from_dict(influencer['Item'])
    
    
  def get_all_influencers(self, limit: int = 10, last_evaluated_key: str = None):
    response = self.dynamo.query(
      index_name='GetAllInfluencersIndex',
      filter_expression=Key('GSI_PK').eq(influencer_gsi_primary_key()),
      limit=limit,
      exclusive_start_key=last_evaluated_key
    )
    
    return {
      'influencers': [Influencer.from_dict(item) for item in response['items']],
      'last_evaluated_key': response.get('last_evaluated_key')
    }

    