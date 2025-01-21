from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX

class CacheWrapper:
    def __init__(self):
        pass

    async def upsert_vault(self, vault: Vault) -> str | None:
        pass

    async def get_vault_by_user_id(self, user_id: int) -> tuple[str | None, Vault | None]:
        pass

    async def get_vault_by_server_ref(self, server_ref: str) -> tuple[str | None, Vault | None]:
        pass

    async def upsert_transaction(self, tx: TX) -> str | None:
        pass

    async def get_transaction(self, tx_id: str) -> tuple[str | None, TX | None]:
        pass

    async def get_vaults_and_lock(self, vaults: list[Vault]) -> None | list[Vault]:
        pass

    async def unlock_vaults(self, vaults: list[Vault]) -> None | list[Vault]:
        pass