from src.shared.environments import Environments
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache
from src.shared.infra.external.elasticache_datasource import ElastiCacheDatasource

class WalletCacheElastic(IWalletCache):
    elastic: ElastiCacheDatasource

    VAULT_EXPIRE_SECS: int = 15

    def __init__(self, elastic: ElastiCacheDatasource):
        self.elastic = elastic

    ### VAULTS ###
    def get_vault_by_user_id(self, user_id: int | str) -> Vault | None:
        vault_id_key = Vault.user_id_to_identity_key(user_id)

        result = self.elastic.redis.hgetall(vault_id_key)

        if len(result) == 0:
            return None

        return Vault.from_redis_hgetall(result)

    def upsert_vault(self, vault: Vault) -> Vault:
        vault_id_key = vault.to_identity_key()
        redis_args = vault.to_redis_upsert_args()

        self.elastic.evalsha(Environments.redis_script_upsert_vault, redis_args)
        self.elastic.expire(vault_id_key, self.VAULT_EXPIRE_SECS)

        return vault
    
    def get_vaults_and_lock(self, vaults: list[Vault]) -> str | list[Vault]:
        lockable_vaults = [ v for v in vaults if v.lockable() ]

        if len(lockable_vaults) == 1:
            result_1p = self.get_lockable_vault_1p(lockable_vaults[0])

            if isinstance(result_1p, bytes):
                return result_1p.decode('utf8')

            cache_vault = Vault.from_redis_hgetall_list(result_1p)

            result_vaults = []

            for vault in vaults:
                if vault.to_identity_key() == cache_vault.to_identity_key():
                    result_vaults.append(cache_vault)
                else:
                    result_vaults.append(vault)

            return result_vaults
        
        if len(lockable_vaults) == 2:
            result_2p = self.get_lockable_vault_2p(lockable_vaults)

            if isinstance(result_2p, bytes):
                return result_2p.decode('utf8')
            
            cache_vaults = {}

            for rv in result_2p:
                cache_vault = Vault.from_redis_hgetall_list(rv)
                cache_vaults[cache_vault.to_identity_key()] = cache_vault

            result_vaults = []

            for vault in vaults:
                vault_id_key = vault.to_identity_key()
                
                if vault_id_key in cache_vaults:
                    result_vaults.append(cache_vaults[vault_id_key])
                else:
                    result_vaults.append(vault)

            return result_vaults
        
        raise Exception(f'Bloqueio de {len(lockable_vaults)} carteiras não foi implementado ainda')

    def get_lockable_vault_1p(self, vault: Vault) -> bytes | list:
        return self.elastic.evalsha(Environments.redis_script_get_lock_vault_1p, [ vault.to_identity_key() ])
    
    def get_lockable_vault_2p(self, vaults: list[Vault]) -> bytes | list[list]:
        return self.elastic.evalsha(Environments.redis_script_get_lock_vault_2p, [ v.to_identity_key() for v in vaults ])
    
    def unlock_vaults(self, vaults: list[Vault]) -> list[Vault]:
        lockable_vaults = [ v for v in vaults if v.lockable() ]

        if len(lockable_vaults) == 1:
            self.unlock_vault_1p(lockable_vaults[0])

        if len(lockable_vaults) == 2:
            self.unlock_vault_2p(lockable_vaults)

        return vaults

    def unlock_vault_1p(self, vault: Vault) -> None:
        return self.elastic.evalsha(Environments.redis_script_unlock_vault_1p, [ vault.to_identity_key() ])
    
    def unlock_vault_2p(self, vaults: list[Vault]) -> None:
        return self.elastic.evalsha(Environments.redis_script_unlock_vault_2p, [ v.to_identity_key() for v in vaults ])