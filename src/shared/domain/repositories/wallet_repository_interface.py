from abc import ABC, abstractmethod

from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

class IWalletRepository(ABC):
    ### USERS ###
    def get_user_by_email(self, email: str) -> User | None:
        pass
        
    ### VAULTS ###
    @abstractmethod
    def create_vault(self, vault: Vault) -> Vault:
        pass

    @abstractmethod
    def get_vault_by_user_id(self, user_id: int | str) -> Vault | None:
        pass
    
    @abstractmethod
    def upsert_vault(self, vault: Vault) -> Vault:
        pass

    ### TRANSACTIONS ###
    @abstractmethod
    def get_transaction_by_id(self, tx_id: str) -> TX | None:
        pass

    @abstractmethod
    def upsert_tx(self, tx: TX) -> TX:
        pass
    
    @abstractmethod
    def get_transactions_by_user(self, user: User | AuthAuthorizerDTO, limit: int = 10, ini_timestamp: int | None = None, \
        end_timestamp: int | None = None, last_evaluated_key: str = None) -> dict:
        pass

    

