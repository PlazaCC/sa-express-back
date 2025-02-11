import os

from src.shared.environments import STAGE, Environments

from src.shared.domain.repositories.entity_repository_interface import IEntityRepository
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache

from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.elasticache_datasource import ElastiCacheDatasource
from src.shared.infra.repositories.auth.auth_repository_cognito import AuthRepositoryCognito
from src.shared.infra.repositories.database.entity_repository_dynamo import EntityRepositoryDynamo
from src.shared.infra.repositories.database.profile_repository_dynamo import ProfileRepositoryDynamo
from src.shared.infra.repositories.mocks.entity_repository_mock import EntityRepositoryMock
from src.shared.infra.repositories.mocks.profile_repository_mock import ProfileRepositoryMock
from src.shared.infra.repositories.database.wallet_repository_dynamo import WalletRepositoryDynamo
from src.shared.infra.repositories.cache.wallet_cache_elastic import WalletCacheElastic
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock
from src.shared.infra.repositories.mocks.wallet_cache_mock import WalletCacheMock

class Repository:
    auth_repo: AuthRepositoryCognito
    profile_repo: IProfileRepository
    entity_repo: IEntityRepository
    wallet_repo: IWalletRepository
    wallet_cache: IWalletCache

    def __init__(
            self,
            auth_repo: bool = False,
            profile_repo: bool = False,
            entity_repo: bool = False,
            wallet_repo: bool = False,
            wallet_cache: bool = False
    ):
        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories(
                profile_repo,
                entity_repo,
                wallet_repo, 
                wallet_cache
            )
        else:
            self._initialize_database_repositories(
                auth_repo,
                profile_repo,
                entity_repo,
                wallet_repo,
                wallet_cache
            )
    
    def _initialize_mock_repositories(self, profile_repo: bool, entity_repo: bool, \
        wallet_repo: bool, wallet_cache: bool) -> None:
        if profile_repo:
            self.profile_repo = ProfileRepositoryMock()
        
        if entity_repo:
            self.entity_repo = EntityRepositoryMock()

        if wallet_repo:
            self.wallet_repo = WalletRepositoryMock(singleton=True)

        if wallet_cache:
            self.wallet_cache = WalletCacheMock(singleton=True)
            
    def _initialize_database_repositories(self, auth_repo: bool, profile_repo: bool, \
        entity_repo: bool, wallet_repo: bool, wallet_cache: bool) -> None:

        dynamo = DynamoDatasource(
            dynamo_table_name=Environments.dynamo_table_name,
            region=Environments.region,
            endpoint_url='http://localhost:8000' if Environments.persist_local else None
        )

        if entity_repo:
            self.entity_repo = EntityRepositoryDynamo(dynamo)
        
        if auth_repo:
            self.auth_repo = AuthRepositoryCognito()
        
        if profile_repo:
            self.profile_repo = ProfileRepositoryDynamo(dynamo)
        
        if entity_repo:
            self.entity_repo = EntityRepositoryDynamo(dynamo)

        if wallet_repo:
            self.wallet_repo = WalletRepositoryDynamo(dynamo)
        
        if wallet_cache:
            elastic = ElastiCacheDatasource(
                region=Environments.region
            )
            
            self.wallet_cache = WalletCacheElastic(elastic)
