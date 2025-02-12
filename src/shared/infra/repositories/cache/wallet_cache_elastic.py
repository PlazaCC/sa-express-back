from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache

from src.shared.infra.external.elasticache_datasource import ElastiCacheDatasource

class WalletCacheElastic(IWalletCache):
    elastic: ElastiCacheDatasource
    
    VAULT_EXPIRE_SECS: int = 5

    def __init__(self, elastic: ElastiCacheDatasource):
        self.elastic = elastic

    ### VAULTS ###
    def get_vault_by_user_id(self, user_id: int | str) -> Vault | None:
        vault_id_key = Vault.user_id_to_identity_key(user_id)

        vault_dict = self.elastic.get_json(vault_id_key)

        return None if vault_dict is None else Vault.from_dict_static(vault_dict)
    
    def upsert_vault(self, vault: Vault) -> Vault:
        vault_id_key = vault.to_identity_key()

        self.elastic.set_json(vault_id_key, vault.to_dict())
        self.elastic.expire(vault_id_key, self.VAULT_EXPIRE_SECS)

        return vault
    
    def get_vaults_and_lock(self, vaults: list[Vault]) -> None | list[Vault]:
        pass
    
    def unlock_vaults(self, vaults: list[Vault]) -> None | list[Vault]:
        pass