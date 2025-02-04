import time
from typing import List
from src.shared.domain.entities.affiliation import Affiliation
from src.shared.domain.entities.deal_proposal import DealProposal, Proposal
from src.shared.domain.entities.profile import Profile
from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS
from src.shared.domain.enums.proposal_type_enum import PROPOSAL_TYPE
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.key_formatters import metadata_sort_key, profile_primary_key

class ProfileRepositoryDynamo(IProfileRepository):
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def get_profile_by_id(self, user_id: str) -> Profile:
        profile = self.dynamo.get_item(
            partition_key=profile_primary_key(user_id), 
            sort_key=metadata_sort_key())
        
        if "Item" not in profile:
            return None
        
        return Profile.from_dict(profile['Item'])

    def create_profile(self, profile: Profile) -> Profile:
        item  = profile.to_dict()
        item["PK"] = profile_primary_key(profile.user_id)
        item["SK"] = metadata_sort_key()    
        
        self.dynamo.put_item(item=item)
        return profile

    def update_profile(self, new_profile: Profile) -> Profile:
        new_profile.updated_at = int(round(time.time() * 1000))
        item = new_profile.to_dict()
        item["PK"] = profile_primary_key(new_profile.user_id)
        item["SK"] = metadata_sort_key()    
        
        self.dynamo.put_item(item=item)
        
        return new_profile