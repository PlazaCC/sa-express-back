import boto3

from src.shared.environments import Environments
from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.repositories.dtos.user_cognito_dto import UserCognitoDTO

class WalletRepositoryDynamo(IWalletRepository):
    dynamo: DynamoDatasource
    client: boto3.client
    user_pool_id: str
    client_id: str

    @staticmethod
    def vault_partition_key_format(vault_id_key: str) -> str:
        return f'VAULT#{vault_id_key}'
    
    @staticmethod
    def vault_sort_key_format() -> str:
        return 'NONE'
    
    @staticmethod
    def tx_partition_key_format(tx_id: str) -> str:
        return f'TX#{tx_id}'
    
    @staticmethod
    def tx_sort_key_format() -> str:
        return 'NONE'

    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

        self.client = boto3.client('cognito-idp', region_name=Environments.region)
        self.user_pool_id = Environments.user_pool_id
        self.client_id = Environments.app_client_id

    ### USERS ###
    def get_user_by_email(self, email: str) -> User | None:
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )

            if response['UserStatus'] == 'UNCONFIRMED':
                return None

            user = UserCognitoDTO.from_cognito(response).to_entity()
                
            return user
        except self.client.exceptions.UserNotFoundException:
            return None

    ### VAULTS ###
    def create_vault(self, vault: Vault) -> Vault:
        vault_id_key = vault.to_identity_key()
        
        item = vault.to_dict(dynamodb=True)
        item['PK'] = self.vault_partition_key_format(vault_id_key)
        item['SK'] = self.vault_sort_key_format()

        self.dynamo.put_item(item=item)

        return vault

    def get_vault_by_user_id(self, user_id: int | str) -> Vault | None:
        vault_id_key = Vault.user_id_to_identity_key(user_id)

        vault = self.dynamo.get_item(
            partition_key=self.vault_partition_key_format(vault_id_key), 
            sort_key=self.vault_sort_key_format()
        )

        return Vault.from_dict_static(vault['Item']) if 'Item' in vault else None
    
    def upsert_vault(self, vault: Vault) -> Vault:
        return self.create_vault(vault)

    ### TRANSACTIONS ###
    def get_transaction(self, tx_id: str) -> TX | None:
        tx = self.dynamo.get_item(
            partition_key=self.tx_partition_key_format(tx_id),
            sort_key=self.tx_sort_key_format()
        )

        return TX.from_dict_static(tx['Item']) if 'Item' in tx else None
    
    def upsert_tx(self, tx: TX) -> TX:
        item = tx.to_dict()
        item['PK'] = self.tx_partition_key_format(tx.tx_id)
        item['SK'] = self.tx_sort_key_format()

        self.dynamo.put_item(item=item)

        return tx