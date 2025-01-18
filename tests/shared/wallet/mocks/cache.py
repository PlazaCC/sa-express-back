import asyncio

from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX

from src.shared.wallet.wrappers.cache import CacheWrapper

class CacheMock(CacheWrapper):
    def __init__(self):
        self.vaults_by_user_id = {}
        self.vaults_by_server_ref = {}
        self.transactions = {}
    
    ### DEBUG-ONLY METHODS ###
    async def get_vault(self, vault: Vault, deserialize: bool = True) -> tuple[str | None, Vault | None]:
        if vault.type == VAULT_TYPE.USER:
            return await self.get_vault_by_user_id(vault.user_id, deserialize)
        
        if vault.type == VAULT_TYPE.SERVER_LIMITED:
            return await self.get_vault_by_server_ref(vault.server_ref, deserialize)
    
    def get_all_vaults(self) -> list[Vault]:
        user_vaults = [ Vault.from_dict_static(self.vaults_by_user_id[vk]) for vk in self.vaults_by_user_id ]
        server_vaults = [ Vault.from_dict_static(self.vaults_by_server_ref[vk]) for vk in self.vaults_by_server_ref ]

        return user_vaults + server_vaults
    
    def get_all_user_vaults(self) -> list[Vault]:
        return [ Vault.from_dict_static(self.vaults_by_user_id[vk]) for vk in self.vaults_by_user_id ]

    ### OVERRIDE METHODS ###
    async def set_vault(self, vault: Vault) -> str | None:
        if vault.user_id is not None:
            self.vaults_by_user_id[vault.user_id] = vault.to_dict()

            return None
        
        if vault.server_ref is not None:
            self.vaults_by_server_ref[vault.server_ref] = vault.to_dict()

            return None

        return "Can't set vault without reference/id"
    
    async def get_vault_by_user_id(self, user_id: int, deserialize: bool = True) -> tuple[str | None, Vault | None]:
        if user_id in self.vaults_by_user_id:
            return None, Vault.from_dict_static(self.vaults_by_user_id[user_id]) if deserialize else self.vaults_by_user_id[user_id]

        return None, None
    
    async def get_vault_by_server_ref(self, server_ref: str, deserialize: bool = True) -> tuple[str | None, Vault | None]:
        if server_ref in self.vaults_by_server_ref:
            return None, Vault.from_dict_static(self.vaults_by_server_ref[server_ref]) if deserialize else self.vaults_by_server_ref[server_ref]
        
        return None, None
    
    async def set_transaction(self, tx: TX) -> str | None:
        self.transactions[tx.tx_id] = tx.to_tx_snapshot()

        return None
    
    async def get_transaction(self, tx_id: str) -> tuple[str | None, TX | None]:
        if tx_id in self.transactions:
            return None, TX.from_tx_snapshot(self.transactions[tx_id])
        
        return None, None

    async def get_vaults_and_lock(self, vaults: list[Vault]) -> None | list[Vault]:
        cache_vaults = []

        async def _get_vault(v: Vault):
            if v.type == VAULT_TYPE.SERVER_UNLIMITED:
                return (None, v.to_dict())
            
            return await self.get_vault(v, deserialize=False)
        
        for (_, cache_vault) in await asyncio.gather(*[ _get_vault(v) for v in vaults ]):
            if cache_vault['locked']:
                return None
            
            cache_vaults.append(cache_vault)

        for cache_vault in cache_vaults:
            cache_vault['locked'] = True

        return [ Vault.from_dict_static(v) for v in cache_vaults ]
    
    async def unlock_vaults(self, vaults: list[Vault]) -> None | list[Vault]:
        cache_vaults = []

        async def _get_vault(v: Vault):
            if v.type == VAULT_TYPE.SERVER_UNLIMITED:
                return (None, v.to_dict())
            
            return await self.get_vault(v, deserialize=False)
        
        for (_, cache_vault) in await asyncio.gather(*[ _get_vault(v) for v in vaults ]):
            cache_vault['locked'] = False

        return [ Vault.from_dict_static(v) for v in cache_vaults ]
    
