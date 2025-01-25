from typing import List
from src.shared.environments import Environments
from src.shared.domain.entities.deal import Deal
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from src.shared.domain.repositories.deal_repository_interface import IDealRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from boto3.dynamodb.conditions import Key

class DealRepositoryDynamo(IDealRepository):

    @staticmethod
    def deal_partition_key_format(deal_id: str) -> str:
        return f'DEAL#{deal_id}'
    
    @staticmethod
    def deal_metadata_sort_key_format() -> str:
        return 'METADATA'
    
    @staticmethod
    def deal_proposal_sort_key_format(status: str, proposal_id: str) -> str:
        return f'PROPOSAL#{status}#{proposal_id}'

    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo
    
    def create_deal(self, deal: Deal) -> Deal:
        item = deal.to_dict()

        self.dynamo.put_item(item=item)

        return deal
    
    def get_deal_by_id(self, deal_id: str) -> Deal:
        deal = self.dynamo.get_item(partition_key=self.deal_partition_key_format(deal_id), sort_key=self.deal_metadata_sort_key_format())

        if "Item" not in deal:
            return None

        return Deal.from_dict(deal['Item'])
    
    def get_all_active_deals(self) -> List[Deal]:
        resp = self.dynamo.query(
            
        )

        deals = []
        for item in resp['Items']:
            deals.append(Deal.from_dict(item))

        return deals
    
    def get_all_deals(self) -> List[Deal]:
        # ALERT: need pagination!!!
        resp = self.dynamo.scan(Select='ALL_ATTRIBUTES')

        deals = []
        for item in resp['Items']:
            deals.append(Deal.from_dict(item))

        return deals
    
    def update_deal(self, deal_id: str, new_deal: Deal) -> Deal:
        # VALIDAR REGRA DE NEGOCIO DE UPDATE DEAL
        pass

    def delete_deal(self, entity_id: str, deal_id: str) -> Deal:
        resp = self.dynamo.delete_item(partition_key=self.deal_partition_key_format(entity_id), sort_key=self.deal_sort_key_format(deal_id))

        if "Attributes" not in resp:
            return None

        return Deal.from_dict(resp['Attributes'])