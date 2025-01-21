from abc import ABC, abstractmethod

from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX

class IWalletCache(ABC):
    ### VAULTS ###
    @abstractmethod
    def get_vault_by_user_id(self, user_id: int | str) -> Vault | None:
        pass

    @abstractmethod
    def get_vault_by_server_ref(self, server_ref: str) -> Vault | None:
        pass
    
    @abstractmethod
    def upsert_vault(self, vault: Vault) -> Vault:
        pass
    
    @abstractmethod
    def get_vaults_and_lock(self, vaults: list[Vault]) -> None | list[Vault]:
        pass
    
    @abstractmethod
    def unlock_vaults(self, vaults: list[Vault]) -> None | list[Vault]:
        pass

    ### TRANSACTIONS ###
    @abstractmethod
    def get_transaction(self, tx_id: str) -> TX | None:
        pass

    @abstractmethod
    def upsert_transaction(self, tx: TX) -> TX:
        pass