from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault

class VaultProcessor:
    def __init__(self):
        pass
    
    def createIfNotExists(self, user: User, config: object) -> Vault:
        # verificar se já existe
        # se sim, retornar vault existente
        # se não, criar vault na db
        # trazer vault pra cache também

        vault = Vault.from_user(1, user, config)

        return vault
