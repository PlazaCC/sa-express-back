from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.repositories.affiliation_repository_interface import IAffiliationRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.key_formatters import affiliation_gsi_primary_key, affiliation_sort_key, profile_primary_key


class AffiliationRepositoryDynamo(IAffiliationRepository):

    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def get_affiliation_by_id(self, user_id) -> Affiliation:
        affiliation = self.dynamo.get_item(partition_key=profile_primary_key(user_id), sort_key=self.affiliation_sort_key_format())
    
        if "Item" not in affiliation:
            return None
    
        return Affiliation.from_dict(affiliation['Item'])
    
    def create_affiliation(self, affiliation: Affiliation, entity_id: str) -> Affiliation:
        item = affiliation.to_dict()
        item["PK"] = profile_primary_key(affiliation.user_id)
        item["SK"] = affiliation_sort_key(affiliation.deal_id)
        item["GSI#AFFILIATION#entityId"] = affiliation_gsi_primary_key(entity_id)
        
        self.dynamo.put_item(item=item)
        return affiliation
        
    def get_all_my_affiliations(self, user_id: str, limit: int = 10, last_evaluated_key: str = None) -> dict:
        resp = self.dynamo.query(
            partition_key=profile_primary_key(user_id),
            sort_key_prefix="AFFILIATION#",
            limit=limit,
            exclusive_start_key=last_evaluated_key
        )

        return {
            "affiliations": [Affiliation.from_dict(item) for item in resp.get("items", [])],
            "last_evaluated_key": resp.get("last_evaluated_key")
        }