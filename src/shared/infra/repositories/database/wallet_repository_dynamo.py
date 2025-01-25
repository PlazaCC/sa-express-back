from src.environments import Environments

from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.vault import Vault
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource

class WalletRepositoryDynamo(IWalletRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def vault_partition_key_format(vault_id_key: str) -> str:
        return vault_id_key
    
    @staticmethod
    def vault_sort_key_format(vault_id_key: str) -> str:
        return vault_id_key
    
    @staticmethod
    def tx_partition_key_format(tx_id: str) -> str:
        return tx_id
    
    @staticmethod
    def tx_sort_key_format(tx_id: str) -> str:
        return tx_id

    def __init__(self):
        self.dynamo = DynamoDatasource(
            dynamo_table_name=Environments.get_envs().dynamo_profile_table_name,
            region=Environments.get_envs().region,
            partition_key=Environments.get_envs().dynamo_profile_partition_key,
            sort_key=Environments.get_envs().dynamo_profile_sort_key,
            gsi_partition_key=Environments.get_envs().dynamo_profile_gsi_partition_key,
        )

    ### VAULTS ###
    def create_vault(self, vault: Vault) -> Vault:
        vault_id_key = vault.to_identity_key()

        self.dynamo.put_item(
            item=vault.to_dict(),
            partition_key=self.vault_partition_key_format(vault_id_key),
            sort_key=self.vault_sort_key_format(vault_id_key),
            is_decimal=True
        )

        return vault

    def get_vault_by_user_id(self, user_id: int | str) -> Vault | None:
        vault_id_key = Vault.user_id_to_identity_key(user_id)

        vault = self.dynamo.get_item(
            partition_key=self.vault_partition_key_format(vault_id_key), 
            sort_key=self.vault_sort_key_format(vault_id_key)
        )

        return Vault.from_dict_static(vault['Item']) if 'Item' in vault else None
    
    def upsert_vault(self, vault: Vault) -> Vault:
        return self.create_vault(vault)

    ### TRANSACTIONS ###
    def get_transaction(self, tx_id: str) -> TX | None:
        tx = self.dynamo.get_item(
            partition_key=self.tx_partition_key_format(tx_id),
            sort_key=self.tx_sort_key_format(tx_id)
        )

        return TX.from_dict_static(tx['Item']) if 'Item' in tx else None
    
    def upsert_tx(self, tx: TX) -> TX:
        self.dynamo.put_item(
            item=tx.to_dict(),
            partition_key=self.tx_partition_key_format(tx.tx_id),
            sort_key=self.tx_sort_key_format(tx.tx_id),
            is_decimal=True
        )

        return tx