import boto3
from boto3.dynamodb.conditions import Attr

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
    def tx_partition_key_format(obj: TX | User) -> str:
        return f'TX#{str(obj.user_id)}'
    
    @staticmethod
    def tx_sort_key_format(obj: TX) -> str:
        return f'TX#{str(obj.create_timestamp)}#{obj.nonce}'

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
    def get_transaction_by_id(self, tx_id: str) -> TX | None:
        resp = self.dynamo.query(
            partition_key=tx_id,
            index_name='TXById'
        )

        items = resp['items']

        return TX.from_dict_static(items[0]) if len(items) > 0 else None
    
    def upsert_tx(self, tx: TX) -> TX:
        item = tx.to_dict()

        item['PK'] = self.tx_partition_key_format(tx)
        item['SK'] = self.tx_sort_key_format(tx)

        self.dynamo.put_item(item=item)

        return tx
    
    def get_transactions_by_user(self, user: User, limit: int = 10, \
        last_evaluated_key: str = None, ini_timestamp: int | None = None, \
        end_timestamp: int | None = None) -> list[TX]:
        filter_expression = None

        if ini_timestamp is not None and end_timestamp is not None:
            filter_expression = Attr('create_timestamp').gte(ini_timestamp) & Attr('create_timestamp').lte(end_timestamp)
        elif ini_timestamp is not None:
            filter_expression = Attr('create_timestamp').gte(ini_timestamp)
        elif end_timestamp is not None:
            filter_expression = Attr('create_timestamp').lte(end_timestamp)

        resp = self.dynamo.query(
            partition_key=self.tx_partition_key_format(user),
            limit=limit,
            filter_expression=filter_expression,
            exclusive_start_key=last_evaluated_key
        )

        return {
            'txs': [ TX.from_dict_static(item) for item in resp['items'] ],
            'last_evaluated_key': resp['last_evaluated_key']
        }