from typing import List
import time
from src.shared.domain.entities.deal import Deal
from src.shared.domain.entities.entity import Entity
from src.shared.domain.repositories.entity_repository_interface import IEntityRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from boto3.dynamodb.conditions import Key, Attr


class EntityRepositoryDynamo(IEntityRepository):

    @staticmethod
    def entity_partition_key_format(entity_id: str) -> str:
        return f'ENTITY#{entity_id}'
    
    @staticmethod
    def entity_metadata_sort_key_format() -> str:
        return 'METADATA'
    
    @staticmethod
    def deal_sort_key_format(deal_id: str, status: str) -> str:
        return f'DEAL#{status}#{deal_id}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo
    
    def get_entity(self, entity_id: str) -> Entity:
        resp = self.dynamo.get_item(partition_key=self.entity_partition_key_format(entity_id), sort_key=self.entity_metadata_sort_key_format())

        if "Item" not in resp:
            return None

        return Entity.from_dict(resp['Item'])
    
    def create_entity(self, entity: Entity) -> Entity:
        item = entity.to_dict()
        item["PK"] = self.entity_partition_key_format(entity.entity_id)
        item["SK"] = self.entity_metadata_sort_key_format()
        item["GSI#ENTITY"] = "GSI#ENTITY"

        self.dynamo.put_item(item=item)

        return entity
    
    def update_entity(self, new_entity: Entity) -> Entity:
        new_entity.updated_at = int(round(time.time() * 1000))
        item = new_entity.to_dict()
        item["PK"] = self.entity_partition_key_format(new_entity.entity_id)
        item["SK"] = self.entity_metadata_sort_key_format()

        self.dynamo.put_item(item=item)

        return new_entity

    def delete_entity(self, entity_id: str) -> Entity:
        resp = self.dynamo.delete_item(partition_key=self.entity_partition_key_format(entity_id), sort_key=self.entity_metadata_sort_key_format())

        if "Attributes" not in resp:
            return None

        return Entity.from_dict(resp['Attributes'])
    
    def get_all_entities(self) -> List[Entity]:

        response = self.dynamo.query(
            partition_key='GSI#ENTITY',
            index_name='AllEntitiesMetadata',
        )

        return [Entity.from_dict(item) for item in response["items"]]

    def create_deal(self, deal: Deal) -> Deal:
        item = deal.to_dict()
        item["PK"] = self.entity_partition_key_format(deal.entity_id)
        item["SK"] = self.deal_sort_key_format(deal_id=deal.deal_id, status=deal.deal_status.value)

        self.dynamo.put_item(item=item)

        return deal

    def get_entity_deals(self, entity_id: str, status: str = None, limit: int = 10, last_evaluated_key: str = None):
        if status:
            sort_key_prefix = f"DEAL#{status}"
        else:
            sort_key_prefix = "DEAL#"

        resp = self.dynamo.query(
            partition_key=self.entity_partition_key_format(entity_id),
            sort_key_prefix=sort_key_prefix,
            limit=limit,
            exclusive_start_key=last_evaluated_key
        )

        return {
            "deals": [Deal.from_dict(item) for item in resp.get("items", [])],
            "last_evaluated_key": resp.get("last_evaluated_key")
        }
    
    def update_deal_status(self, deal: Deal, new_status: str) -> Deal:
        self.dynamo.delete_item(
            partition_key=self.entity_partition_key_format(deal.entity_id),
            sort_key=self.deal_sort_key_format(deal.deal_id, deal.old_status)
        )

        deal_data = deal.to_dict()

        deal_data["PK"] = self.entity_partition_key_format(deal.entity_id)
        deal_data["SK"] = self.deal_sort_key_format(deal.deal_id, new_status)
        self.dynamo.put_item(item=deal_data)

        return Deal.from_dict(deal_data)

