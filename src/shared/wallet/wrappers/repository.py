from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX

class RepositoryWrapper:
    def __init__(self):
        pass

    ### VAULTS ###
    def create_vault(self, vault: Vault) -> Vault:
        pass

    def get_vault_by_user_id(self, user_id: int) -> Vault | None:
        pass

    def get_vault_by_sever_ref(self, server_ref: str) -> Vault | None:
        pass
    
    def upsert_vault(self, vault: Vault) -> Vault:
        pass

    ### TRANSACTIONS ###
    def get_transaction(self, tx_id: str) -> TX | None:
        pass

    def upsert_transaction(self, tx: TX) -> TX:
        pass

