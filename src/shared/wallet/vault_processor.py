from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

class VaultProcessor:
    cache: IWalletCache
    repository: IWalletRepository

    def __init__(self, cache: IWalletCache, repository: IWalletRepository):
        self.cache = cache
        self.repository = repository
    
    def create_if_not_exists(self, user: User | AuthAuthorizerDTO, config: dict = Vault.default_config()) -> Vault:
        cache_vault = self.cache.get_vault_by_user_id(user.user_id)

        if cache_vault is not None:
            return cache_vault
        
        rep_vault = self.repository.get_vault_by_user_id(user.user_id)

        if rep_vault is not None:
            self.cache.upsert_vault(rep_vault)

            return rep_vault
        
        vault = Vault.from_user(user, config)
        
        self.cache.upsert_vault(vault)
        self.repository.create_vault(vault)
        
        return vault
    
    def get_by_user(self, user: User | AuthAuthorizerDTO) -> Vault | None:
        cache_vault = self.cache.get_vault_by_user_id(user.user_id)

        if cache_vault is not None:
            return cache_vault
        
        rep_vault = self.repository.get_vault_by_user_id(user.user_id)

        if rep_vault is not None:
            self.cache.upsert_vault(rep_vault)

            return rep_vault
        
        return None
    
    def persist_vault(self, vault: Vault) -> None:
        self.cache.upsert_vault(vault)
        self.repository.upsert_vault(vault)

        return None

    def get_and_lock(self, vaults: list[Vault]) -> None | list[Vault]:
        return self.cache.get_vaults_and_lock(vaults)

    def unlock(self, vaults: Vault | list[Vault]) -> list[Vault]:
        return self.cache.unlock_vaults(vaults)


    
