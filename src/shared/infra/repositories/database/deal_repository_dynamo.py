from src.shared.domain.entities.deal import Deal
from src.shared.domain.repositories.deal_repository_interface import IDealRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.key_formatters import deal_sort_key, entity_primary_key


class DealRepositoryDynamo(IDealRepository):

    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create_deal(self, deal: Deal) -> Deal:
        item = deal.to_dict()
        item["PK"] = entity_primary_key(deal.entity_id)
        item["SK"] = deal_sort_key(deal_id=deal.deal_id, status=deal.deal_status.value)

        self.dynamo.put_item(item=item)

        return deal

    def get_entity_deals(self, entity_id: str, status: str = None, limit: int = 10, last_evaluated_key: str = None):
        if status:
            sort_key_prefix = f"DEAL#{status}"
        else:
            sort_key_prefix = "DEAL#"

        resp = self.dynamo.query(
            partition_key=entity_primary_key(entity_id),
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
            partition_key=entity_primary_key(deal.entity_id),
            sort_key=deal_sort_key(deal.deal_id, deal.old_status)
        )

        deal_data = deal.to_dict()
        deal_data["deal_status"] = new_status

        deal_data["PK"] = entity_primary_key(deal.entity_id)
        deal_data["SK"] = deal_sort_key(deal.deal_id, new_status)
        self.dynamo.put_item(item=deal_data)

        return Deal.from_dict(deal_data)