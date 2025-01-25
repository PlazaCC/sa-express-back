from abc import abstractmethod
from typing import List
from src.shared.domain.entities.profile import Profile
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo_datasource import DynamoDatasource

class ProfileRepositoryDynamo(IProfileRepository):
    
    @staticmethod
    def profile_partition_key_format(user_id: str) -> str:
        return f'PROFILE#{user_id}'
    
    @staticmethod
    def profile_sort_key_format() -> str:
        return f'METADATA'
    
    def __init__(self):
        self.dynamo = DynamoDatasource(
            dynamo_table_name=Environments.get_envs().dynamo_table_name,
            region=Environments.get_envs().region,
            partition_key=Environments.get_envs().dynamo_partition_key,
            sort_key=Environments.get_envs().dynamo_sort_key,
            gsi_partition_key=Environments.get_envs().dynamo_gsi_partition_key,
        )

    @abstractmethod
    def get_profile_by_id(self, user_id: str) -> Profile:
        try:
            profile = self.dynamo.get_item(partition_key=self.profile_partition_key_format(user_id))
            
            if "Item" not in profile:
                return None
            
            return Profile.from_dict(profile['Item'])
        except Exception as e:
            raise e
    
    @abstractmethod
    def create_profile(self, profile: Profile) -> Profile:
        try:
            self.dynamo.put_item(
                item=profile.to_dict(),
                partition_key=self.profile_partition_key_format(profile.user_id),
                sort_key=self.profile_sort_key_format()
            )
            return profile
        except Exception as e:
            raise e
    
    @abstractmethod
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