from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault

class VaultProcessor:
    def __init__(self, cache, repository):
        self.cache = cache
        self.repository = repository
    
    async def create_if_not_exists(self, user: User, config: object) -> Vault:
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
