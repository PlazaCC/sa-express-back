from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX

class RepositoryWrapper:
    def __init__(self):
        pass

    async def set_vault(self, vault: Vault) -> str | None:
        pass

    async def get_vault_by_user_id(self, user_id: int) -> tuple[str | None, Vault | None]:
        pass

    async def get_vault_by_sever_ref(self, server_ref: str) -> tuple[str | None, Vault | None]:
        pass

    async def set_transaction(self, tx: TX) -> str | None:
        pass

    async def get_transaction(self, tx_id: str) -> tuple[str | None, TX | None]:
        pass