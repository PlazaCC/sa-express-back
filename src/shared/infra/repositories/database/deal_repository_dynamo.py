from typing import List
from src.shared.environments import Environments
from src.shared.domain.entities.deal import Deal
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from src.shared.domain.repositories.deal_repository_interface import IDealRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from boto3.dynamodb.conditions import Key

class DealRepositoryDynamo(IDealRepository):

    @staticmethod
    def deal_partition_key_format(bet_id: str) -> str:
        return f'{bet_id}'
    
    @staticmethod
    def deal_sort_key_format(deal_id: str) -> str:
        return f'{deal_id}'
    
    @staticmethod
    def gsi_deal_partition_key_format(deal_status: DEAL_STATUS) -> str:
        return f'{deal_status.value}'

    def __init__(self):
        self.dynamo = DynamoDatasource(
            dynamo_table_name=Environments.get_envs().dynamo_table_name,
            region=Environments.get_envs().region,
            partition_key=Environments.get_envs().dynamo_partition_key,
            sort_key=Environments.get_envs().dynamo_sort_key,
            gsi_partition_key=Environments.get_envs().dynamo_gsi_partition_key,
        )
    
    def create_deal(self, deal: Deal) -> Deal:
        item = deal.to_dict()

        self.dynamo.put_item(item=item, partition_key=self.deal_partition_key_format(deal.bet_id), sort_key=self.deal_sort_key_format(deal.deal_id), is_decimal=True)

        return deal
    
    def get_deal_by_id(self, bet_id: str, deal_id: str) -> Deal:
        deal = self.dynamo.get_item(partition_key=self.deal_partition_key_format(bet_id), sort_key=self.deal_sort_key_format(deal_id))

        if "Item" not in deal:
            return None

        return Deal.from_dict(deal['Item'])
    
    def get_all_active_deals(self) -> List[Deal]:
        query_string = Key(self.dynamo.gsi_partition_key).eq(self.gsi_deal_partition_key_format(DEAL_STATUS.ACTIVE))
        resp = self.dynamo.query(key_condition_expression=query_string, Select='ALL_ATTRIBUTES', IndexName="GSI")

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

    def delete_deal(self, bet_id: str, deal_id: str) -> Deal:
        resp = self.dynamo.delete_item(partition_key=self.deal_partition_key_format(bet_id), sort_key=self.deal_sort_key_format(deal_id))

        if "Attributes" not in resp:
            return None

        return Deal.from_dict(resp['Attributes'])