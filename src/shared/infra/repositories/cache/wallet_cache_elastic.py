from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache

from src.shared.infra.external.elasticache_datasource import ElastiCacheDatasource

class WalletCacheElastic(IWalletCache):
    elastic: ElastiCacheDatasource

    def __init__(self, elastic: ElastiCacheDatasource):
        self.elastic = elastic

    ### VAULTS ###
    def get_vault_by_user_id(self, user_id: int | str) -> Vault | None:
        pass
    
    def upsert_vault(self, vault: Vault) -> Vault:
        pass
    
    def get_vaults_and_lock(self, vaults: list[Vault]) -> None | list[Vault]:
        pass
    
    def unlock_vaults(self, vaults: list[Vault]) -> None | list[Vault]:
        pass