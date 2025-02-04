from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.key_formatters import tx_primary_key, tx_sort_key, vault_primary_key, vault_sort_key

class WalletRepositoryDynamo(IWalletRepository):
    dynamo: DynamoDatasource

    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    ### VAULTS ###
    def create_vault(self, vault: Vault) -> Vault:
        vault_id_key = vault.to_identity_key()

        self.dynamo.put_item(
            item=vault.to_dict(),
            partition_key=vault_primary_key(vault_id_key),
            sort_key=vault_sort_key(vault_id_key),
            is_decimal=True
        )

        return vault

    def get_vault_by_user_id(self, user_id: int | str) -> Vault | None:
        vault_id_key = Vault.user_id_to_identity_key(user_id)

        vault = self.dynamo.get_item(
            partition_key=vault_primary_key(vault_id_key), 
            sort_key=vault_sort_key(vault_id_key)
        )

        return Vault.from_dict_static(vault['Item']) if 'Item' in vault else None
    
    def upsert_vault(self, vault: Vault) -> Vault:
        return self.create_vault(vault)

    ### TRANSACTIONS ###
    def get_transaction(self, tx_id: str) -> TX | None:
        tx = self.dynamo.get_item(
            partition_key=tx_primary_key(tx_id),
            sort_key=tx_sort_key(tx_id)
        )

        return TX.from_dict_static(tx['Item']) if 'Item' in tx else None
    
    def upsert_tx(self, tx: TX) -> TX:
        self.dynamo.put_item(
            item=tx.to_dict(),
            partition_key=tx_primary_key(tx.tx_id),
            sort_key=tx_sort_key(tx.tx_id),
            is_decimal=True
        )

        return tx