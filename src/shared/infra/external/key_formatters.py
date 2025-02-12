from src.shared.domain.enums.proposal_status_enum import PROPOSAL_STATUS
from src.shared.domain.enums.proposal_type_enum import PROPOSAL_TYPE


def profile_primary_key(user_id: str) -> str:
    return f'PROFILE#{user_id}'

def influencer_primary_key(user_id: str) -> str:
    return profile_primary_key(user_id)

def influencer_sort_key() -> str:
    return f'INFLUENCER#{metadata_sort_key()}'

def influencer_gsi_primary_key() -> str:
    return f'INFLUENCER#METADATA'

def metadata_sort_key() -> str:
    return f'METADATA'

def entity_primary_key(entity_id: str) -> str:
    return f'ENTITY#{entity_id}'

def deal_sort_key(deal_id: str, status: str) -> str:
    return f'DEAL#{status}#{deal_id}'

def affiliation_sort_key(deal_id: str) -> str:
    return f'AFFILIATION#{deal_id}'

def affiliation_gsi_primary_key(entityId: str) -> str:
    return f'GSI#AFFILIATION#{entityId}'

def proposal_sort_key(proposal_type: PROPOSAL_TYPE, status: PROPOSAL_STATUS) -> str:
    return f'PROPOSAL#{proposal_type.value}#{status.value}'

def proposal_gsi_receiver_primary_key(proposal_type: PROPOSAL_TYPE, receiver_id: str) -> str:
    # RECEIVER#<DEAL/MENTORSHIP/INFLUENCER>#<UserId/EntityId>
    return f'RECEIVER#{proposal_type.value}#{receiver_id}'

def proposal_gsi_receiver_sort_key(status: PROPOSAL_STATUS, created_at: int) -> str:
    return f'{status.value}#{created_at}'

def vault_primary_key(vault_id_key: str) -> str:
    return vault_id_key

def vault_sort_key(vault_id_key: str) -> str:
    return vault_id_key

def tx_primary_key(tx_id: str) -> str:
    return tx_id

def tx_sort_key(tx_id: str) -> str:
    return tx_id