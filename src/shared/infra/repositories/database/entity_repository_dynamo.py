from typing import List
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
    def deal_sort_key_format(deal_id: str) -> str:
        return f'DEAL#{deal_id}'
    
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

        self.dynamo.put_item(item=item)

        return entity
    
    def create_deal(self, entity_id: str, deal: Deal) -> Deal:
        item = deal.to_dict()
        item["PK"] = self.entity_partition_key_format(entity_id)
        item["SK"] = self.deal_sort_key_format(deal.deal_id)

        self.dynamo.put_item(item=item)

        return deal
    
    def update_entity(self, new_entity: Entity) -> Entity:
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
        key_config = self.dynamo._get_key_config()
        partition_key = Key(key_config["partition_key"]).begins_with("ENTITY#")

        response = self.dynamo.query(
            partition_key=partition_key,
            filter_expression=Attr(key_config["sort_key"]).eq("METADATA")  # Filtra para pegar apenas entidades
        )

        return [Entity.from_dict(item) for item in response["items"]]

