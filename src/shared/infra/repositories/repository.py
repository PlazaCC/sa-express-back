from src.shared.domain.repositories.entity_repository_interface import IEntityRepository
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository
from src.shared.environments import STAGE, Environments
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.repositories.auth.auth_repository_cognito import AuthRepositoryCognito
from src.shared.infra.repositories.database.entity_repository_dynamo import EntityRepositoryDynamo
from src.shared.infra.repositories.database.profile_repository_dynamo import ProfileRepositoryDynamo
from src.shared.infra.repositories.mocks.entity_repository_mock import EntityRepositoryMock
from src.shared.infra.repositories.mocks.profile_repository_mock import ProfileRepositoryMock


class Repository:
    auth_repo: AuthRepositoryCognito
    profile_repo: IProfileRepository
    entity_repo: IEntityRepository

    def __init__(
            self,
            auth_repo: bool = False,
            profile_repo: bool = False,
            entity_repo: bool = False
    ):
        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories(
                profile_repo,
                entity_repo
            )
        else:
            self._initialize_database_repositories(
                auth_repo,
                profile_repo,
                entity_repo
            )
            

    def _initialize_mock_repositories(self, profile_repo, entity_repo):
        if profile_repo:
            self.profile_repo = ProfileRepositoryMock()
        if entity_repo:
            self.entity_repo = EntityRepositoryMock()
            
    def _initialize_database_repositories(self, auth_repo, profile_repo, entity_repo):
        dynamo = DynamoDatasource(
            dynamo_table_name=Environments.dynamo_table_name,
            region=Environments.region,
        )
        if entity_repo:
            self.entity_repo = EntityRepositoryDynamo(dynamo)
        if auth_repo:
            self.auth_repo = AuthRepositoryCognito()
        if profile_repo:
            self.profile_repo = ProfileRepositoryDynamo(dynamo)
        if entity_repo:
            self.entity_repo = EntityRepositoryDynamo(dynamo)