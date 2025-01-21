from abc import abstractmethod
from typing import List
from src.shared.domain.entities.profile import Profile
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo_datasource import DynamoDatasource

class ProfileRepositoryDynamo(IProfileRepository):
    
    @staticmethod
    def profile_partition_key_format(user_id: str) -> str:
        return f'{user_id}'
    
    @staticmethod
    def profile_sort_key_format() -> str:
        return f'PROFILE'
    
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
        profile = self.dynamo.get_item(partition_key=self.profile_partition_key_format(user_id))
        
        if "Item" not in profile:
            return None
        
        return Profile.from_dict(profile['Item'])