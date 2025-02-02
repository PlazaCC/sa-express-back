import time
from typing import List
from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.entities.profile import Profile
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo_datasource import DynamoDatasource

class ProfileRepositoryDynamo(IProfileRepository):
    
    @staticmethod
    def profile_partition_key_format(user_id: str) -> str:
        return f'PROFILE#{user_id}'
    
    @staticmethod
    def profile_metadata_sort_key_format() -> str:
        return f'METADATA'
    
    @staticmethod
    def affiliation_sort_key_format(deal_id: str) -> str:
        return f'AFFILIATION#{deal_id}'
    
    @staticmethod
    def affiliation_gsi_primary_key_format(entityId: str) -> str:
        return f'GSI#AFFILIATION#{entityId}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def get_profile_by_id(self, user_id: str) -> Profile:
        profile = self.dynamo.get_item(partition_key=self.profile_partition_key_format(user_id), sort_key=self.profile_metadata_sort_key_format())
        
        if "Item" not in profile:
            return None
        
        return Profile.from_dict(profile['Item'])

    def create_profile(self, profile: Profile) -> Profile:
        item  = profile.to_dict()
        item["PK"] = self.profile_partition_key_format(profile.user_id)
        item["SK"] = self.profile_metadata_sort_key_format()    
        
        self.dynamo.put_item(item=item)
        return profile

    def update_profile(self, new_profile: Profile) -> Profile:
        new_profile.updated_at = int(round(time.time() * 1000))
        item = new_profile.to_dict()
        item["PK"] = self.profile_partition_key_format(new_profile.user_id)
        item["SK"] = self.profile_metadata_sort_key_format()    
        
        self.dynamo.put_item(item=item)
        
        return new_profile
        
    def get_affiliation_by_id(self, user_id) -> Affiliation:
        affiliation = self.dynamo.get_item(partition_key=self.profile_partition_key_format(user_id), sort_key=self.affiliation_sort_key_format())
    
        if "Item" not in affiliation:
            return None
    
        return Affiliation.from_dict(affiliation['Item'])
    
    def create_affiliation(self, affiliation: Affiliation, entity_id: str) -> Affiliation:
        item = affiliation.to_dict()
        item["PK"] = self.profile_partition_key_format(affiliation.user_id)
        item["SK"] = self.affiliation_sort_key_format(affiliation.deal_id)
        item["GSI#AFFILIATION#entityId"] = self.affiliation_gsi_primary_key_format(entity_id)
        
        self.dynamo.put_item(item=item)
        return affiliation
        
    def get_all_my_affiliations(self, user_id: str, limit: int = 10, last_evaluated_key: str = None):
        resp = self.dynamo.query(
            partition_key=self.profile_partition_key_format(user_id),
            sort_key_prefix="AFFILIATION#",
            limit=limit,
            exclusive_start_key=last_evaluated_key
        )

        return {
            "affiliations": [Affiliation.from_dict(item) for item in resp.get("items", [])],
            "last_evaluated_key": resp.get("last_evaluated_key")
        }