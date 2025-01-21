import asyncio

from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository

from src.shared.wallet.wrappers.cache import CacheWrapper

class VaultProcessor:
    cache: CacheWrapper
    repository: IWalletRepository

    def __init__(self, cache: CacheWrapper, repository: IWalletRepository):
        self.cache = cache
        self.repository = repository
    
    async def create_if_not_exists(self, user: User, config: dict) -> Vault:
        (_, cache_vault) = await self.cache.get_vault_by_user_id(user.user_id)

        if cache_vault is not None:
            return cache_vault
        
        rep_vault = self.repository.get_vault_by_user_id(user.user_id)

        if rep_vault is not None:
            return rep_vault
        
        vault = Vault.from_user(user, config)
        
        self.repository.create_vault(vault)

        await self.cache.upsert_vault(vault)

        return vault
    
    async def persist_vault(self, vault: Vault) -> None:
        self.repository.upsert_vault(vault)

        await self.cache.upsert_vault(vault)

        return None

    async def get_and_lock(self, vaults: list[Vault]) -> None | list[Vault]:
        return await self.cache.get_vaults_and_lock(vaults)

    async def unlock(self, vaults: Vault | list[Vault]) -> list[Vault]:
        return await self.cache.unlock_vaults(vaults)


    
