from src.shared.domain.entities.entity import Entity
from src.shared.domain.repositories.entity_repository_interface import IEntityRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo_datasource import DynamoDatasource


class EntityRepositoryDynamo(IEntityRepository):
  
  @staticmethod
  def entity_partition_key_format(entity_id: str) -> str:
    return f'ENTITY#{entity_id}'
  
  @staticmethod
  def entity_sort_key_format() -> str:
    return f'METADATA'
  
  def __init__(self, dynamo: DynamoDatasource):
    self.dynamo = dynamo
    
  def create_entity(self, entity: Entity):
    try:
      self.dynamo.put_item(
        item=entity.to_dict(),
        partition_key=self.entity_partition_key_format(entity.entity_id),
        sort_key=self.entity_sort_key_format()
      )
      return entity
    except Exception as e:
      raise e
    
  def get_entity_by_id(self, entity_id: str):
    try:
      entity = self.dynamo.get_item(partition_key=self.entity_partition_key_format(entity_id))
      
      if "Item" not in entity:
        return None
      
      return Entity.from_dict(entity['Item'])
    except Exception as e:
      raise e