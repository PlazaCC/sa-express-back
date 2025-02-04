from typing import List
import time
from src.shared.domain.entities.deal import Deal
from src.shared.domain.entities.entity import Entity
from src.shared.domain.repositories.entity_repository_interface import IEntityRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from boto3.dynamodb.conditions import Key, Attr

from src.shared.infra.external.key_formatters import entity_primary_key, metadata_sort_key


class EntityRepositoryDynamo(IEntityRepository):
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo
    
    def get_entity(self, entity_id: str) -> Entity:
        resp = self.dynamo.get_item(partition_key=entity_primary_key(entity_id), 
                                    sort_key=metadata_sort_key())

        if "Item" not in resp:
            return None

        return Entity.from_dict(resp['Item'])
    
    def create_entity(self, entity: Entity) -> Entity:
        item = entity.to_dict()
        item["PK"] = entity_primary_key(entity.entity_id)
        item["SK"] = metadata_sort_key()
        item["GSI#ENTITY"] = "GSI#ENTITY"

        self.dynamo.put_item(item=item)

        return entity
    
    def update_entity(self, new_entity: Entity) -> Entity:
        new_entity.updated_at = int(round(time.time() * 1000))
        item = new_entity.to_dict()
        item["PK"] = entity_primary_key(new_entity.entity_id)
        item["SK"] = metadata_sort_key()

        self.dynamo.put_item(item=item)

        return new_entity

    def delete_entity(self, entity_id: str) -> Entity:
        resp = self.dynamo.delete_item(partition_key=entity_primary_key(entity_id), sort_key=metadata_sort_key())

        if "Attributes" not in resp:
            return None

        return Entity.from_dict(resp['Attributes'])
    
    def get_all_entities(self) -> List[Entity]:

        response = self.dynamo.query(
            partition_key='GSI#ENTITY',
            index_name='AllEntitiesMetadata',
        )

        return [Entity.from_dict(item) for item in response["items"]]

