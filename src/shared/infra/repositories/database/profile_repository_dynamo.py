from abc import abstractmethod
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
    def affiliation_sort_key_format(deal_id) -> str:
        return f'AFFILIATION#{deal_id}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def get_profile_by_id(self, user_id: str) -> Profile:
        try:
            profile = self.dynamo.get_item(partition_key=self.profile_partition_key_format(user_id))
            
            if "Item" not in profile:
                return None
            
            return Profile.from_dict(profile['Item'])
        except Exception as e:
            raise e
    
    def create_profile(self, profile: Profile) -> Profile:
        try:
            profile_to_dynamo = profile.to_dict()            
            profile_to_dynamo.pop("affiliations", None)
            profile_to_dynamo.pop("game_data_id", None)
            
            self.dynamo.put_item(
                item=profile_to_dynamo,
                partition_key=self.profile_partition_key_format(profile.user_id),
                sort_key=self.profile_metadata_sort_key_format()
            )
            return profile
        except Exception as e:
            raise e
    
    def deactivate_profile(self, user_id):
        try:
            profile = self.get_profile_by_id(user_id)
            profile.status = "INACTIVE"
            self.dynamo.update_item(
                partition_key=self.profile_partition_key_format(user_id),
                update_dict=profile.to_dict(),
                sort_key=self.profile_sort_key_format()
            )
            
            return profile
        
        except Exception as e:
            raise e
        
    def get_affiliation_by_id(self, user_id) -> Affiliation:
        try:
            affiliation = self.dynamo.get_item(partition_key=self.profile_partition_key_format(user_id), sort_key=self.affiliation_sort_key_format())
        
            if "Item" not in affiliation:
                return None
        
            return Affiliation.from_dict(affiliation['Item'])
        except Exception as e:
            raise e
    
    def create_affiliation(self, affiliation) -> Affiliation:
        try:
            item = affiliation.to_dict()
            item["PK"] = self.profile_partition_key_format(affiliation.user_id)
            item["SK"] = self.affiliation_sort_key_format(affiliation.deal_id)
            
            self.dynamo.put_item(item=item,)
            return affiliation
        except Exception as e:
            raise e
        
    def get_all_my_affiliations(self, user_id) -> List[Affiliation]:
        try:
            affiliations = self.dynamo.query(
                partition_key=self.profile_partition_key_format(user_id), 
                sort_key=self.affiliation_sort_key_format()
            )
        
            if "Items" not in affiliations:
                return []
            
            return [Affiliation.from_dict(affiliation) for affiliation in affiliations['Items']]
        except Exception as e:
            raise e