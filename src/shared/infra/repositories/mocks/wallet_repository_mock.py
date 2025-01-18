from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.deal_repository_interface import IDealRepository

class WalletRepositoryMock(IDealRepository):
    txs: list[TX]
    users: list[User]
    vaults: list[Vault]

    def __init__(self):
        self.txs = []
        self.users = []
        self.vaults = []
    