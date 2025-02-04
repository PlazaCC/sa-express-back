from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache

class WalletCacheMock(IWalletCache):
    vaults_by_user_id: dict = {}
    transactions: dict = {}

    def __init__(self, singleton=False):
        self.vaults_by_user_id = WalletCacheMock.vaults_by_user_id
        self.transactions = WalletCacheMock.transactions

        if not singleton:
            self.vaults_by_user_id = {}
            self.transactions = {}
    
    ### OVERRIDE METHODS ###
    def upsert_vault(self, vault: Vault) -> Vault:
        if vault.user_id is not None:
            self.vaults_by_user_id[vault.user_id] = vault.to_dict()

        return vault
    
    def get_vault_by_user_id(self, user_id: int | str, deserialize: bool = True) -> Vault | None:
        if user_id in self.vaults_by_user_id:
            return Vault.from_dict_static(self.vaults_by_user_id[user_id]) if deserialize else self.vaults_by_user_id[user_id]

        return None
    
    def upsert_transaction(self, tx: TX) -> TX:
        self.transactions[tx.tx_id] = tx.to_dict()

        return None
    
    def get_transaction(self, tx_id: str) -> TX | None:
        return TX.from_tx_snapshot(self.transactions[tx_id]) if tx_id in self.transactions else None

    def get_vaults_and_lock(self, vaults: list[Vault]) -> None | list[Vault]:
        cache_vaults = []

        def _get_vault(v: Vault):
            if v.type == VAULT_TYPE.SERVER_UNLIMITED:
                v.locked = False

                return v.to_dict()
            
            return self.get_vault(v, deserialize=False)
        
        for cache_vault in ([ _get_vault(v) for v in vaults ]):
            if cache_vault['locked']:
                return None
            
            cache_vaults.append(cache_vault)
        
        for cache_vault in cache_vaults:
            cache_vault['locked'] = True

        return [ Vault.from_dict_static(v) for v in cache_vaults ]
    
    def unlock_vaults(self, vaults: list[Vault]) -> None | list[Vault]:
        cache_vaults = []

        def _get_vault(v: Vault):
            if v.type == VAULT_TYPE.SERVER_UNLIMITED:
                return v.to_dict()
            
            return self.get_vault(v, deserialize=False)

        for cache_vault in ([ _get_vault(v) for v in vaults ]):
            cache_vault['locked'] = False

        return [ Vault.from_dict_static(v) for v in cache_vaults ]
    
    ### DEBUG-ONLY METHODS ###
    def get_vault(self, vault: Vault, deserialize: bool = True) -> Vault | None:
        if vault.type == VAULT_TYPE.USER:
            return self.get_vault_by_user_id(vault.user_id, deserialize)
        
        return None
    
    def get_all_vaults(self) -> list[Vault]:
        user_vaults = [ Vault.from_dict_static(self.vaults_by_user_id[vk]) for vk in self.vaults_by_user_id ]

        return user_vaults
    
    def get_all_user_vaults(self) -> list[Vault]:
        return [ Vault.from_dict_static(self.vaults_by_user_id[vk]) for vk in self.vaults_by_user_id ]
    
