from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.deal_repository_interface import IDealRepository

class WalletRepositoryMock(IDealRepository):
    users: list[User]
    vaults: list[Vault]
    transactions: list[TX]

    def __init__(self):
        self.users = []
        self.vaults = []
        self.transactions = []
    