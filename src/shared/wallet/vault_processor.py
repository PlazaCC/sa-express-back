import asyncio

from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault

class VaultProcessor:
    def __init__(self, cache, repository):
        self.cache = cache
        self.repository = repository
    
    async def create_if_not_exists(self, user: User, config: dict) -> Vault:
        (cache_error, cache_vault) = await self.cache.get_vault_by_user_id(user.user_id)

        if cache_error is not None:
            return cache_error, None

        if cache_vault is not None:
            return None, cache_vault
        
        (rep_error, rep_vault) = await self.repository.get_vault_by_user_id(user.user_id)

        if rep_error is not None:
            return rep_error, None
        
        if rep_vault is not None:
            await self.cache.set_vault(rep_vault)

            return None, rep_vault
        
        vault = Vault.from_user(user, config)

        (set_rep_error, _) = await self.repository.set_vault(vault)

        if set_rep_error is not None:
            return set_rep_error, None

        await self.cache.set_vault(vault)

        return None, vault
    
    def filter_lockable_vaults(self, vaults: list[Vault]):
        return [ v for v in vaults if v.type != VAULT_TYPE.SERVER_UNLIMITED ]
    
    async def lock_all(self, vaults: list[Vault]):
        lockable_vaults = self.filter_lockable_vaults(vaults)

        if len(lockable_vaults) == 0:
            return

        await asyncio.gather(*[ self.cache.lock_vault(v) for v in lockable_vaults ])

    async def unlock_all(self, vaults: list[Vault]):
        lockable_vaults = self.filter_lockable_vaults(vaults)

        if len(lockable_vaults) == 0:
            return
        
        await asyncio.gather(*[ self.cache.unlock_vault(v) for v in lockable_vaults ])

